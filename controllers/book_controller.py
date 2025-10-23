from flask import jsonify, request

from db import db
from models.book import Books

def add_book():
    post_data = request.form if request.form else request.get_json()

    fields = ['school_id', 'title', 'author', 'subject', 'rarity_level', 'magical_properties', 'available']
    required_fields =['school_id', 'title']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_book = Books(values['school_id'], values['title'], values['author'], values['subject'], values['rarity_level'],values['magical_properties'], values['available']) 

    try:
        db.session.add(new_book)
        db.session.commit()
    except: 
        db.session.rollback()
        return jsonify({"message": "unable to create record."}), 400 

    query = db.session.query(Books).filter(Books.title == values['title']).first()

    book = {
        "school_id": query.school_id,
        "title": query.title,
        "author": query.author,
        "subject": query.subject,
        "rarity_level":query.rarity_level,
        "magical_properties":query.magical_properties,
        "available":query.available
    }

    return jsonify({"message":"book created", "result":book}), 201

# ===========================

def get_all_Books():
    query = db.session.query(Books).all()

    

    book_list = []

    for book in query:
       
        book_dict = {
        "book_id" : book.book_id,
        "school_id": book.school_id,
        "title": book.title,
        "author": book.author,
        "subject": book.subject,
        "rarity_level":book.rarity_level,
        "magical_properties":book.magical_properties,
        "available":book.available,
        }
        book_list.append(book_dict)

    return jsonify({"message": "Books founded.", "results": book_list}), 200

# ============================

def get_available_Books():
    query = db.session.query(Books).filter(Books.available).all()
    if not query:
        return jsonify({"message": "no available book found"}), 404
    
    available_book_list = []
    for book in query:
        available_book_dict = {
        "book_id" : book.book_id,
        "school_id": book.school_id,
        "title": book.title,
        "author": book.author,
        "subject": book.subject,
        "rarity_level":book.rarity_level,
        "magical_properties":book.magical_properties,
        "available":book.available
        }
        available_book_list.append(available_book_dict)

    return jsonify({"message": "Available books found", "results": available_book_list}), 200

# ===========================


def update_book_by_id(book_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Books).filter(Books.book_id==book_id).first()

    if not query:
        return jsonify({"message": "book not found"}), 404

    query.title = post_data.get("title", query.title)
    query.author = post_data.get("author", query.author)
    query.subject = post_data.get("subject", query.subject)
    query.rarity_level = post_data.get("rarity_level", query.rarity_level)
    query.magical_properties = post_data.get("magical_properties", query.magical_properties)
    query.available = post_data.get("available", query.available)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}),400

    
    update_book_query = db.session.query(Books).filter(Books.book_id==book_id).first()

    book={
        "book_id" : update_book_query.book_id,
        "school_id": update_book_query.school_id,
        "title": update_book_query.title,
        "author": update_book_query.author,
        "subject": update_book_query.subject,
        "rarity_level":update_book_query.rarity_level,
        "magical_properties":update_book_query.magical_properties,
        "available":update_book_query.available
    }

    return jsonify ({"message": "record updated.", "result": update_book_query}), 200

# ===============================

def delete_book_by_id(book_id):
    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    if not query:
        return jsonify({"message": "book not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete book"}), 400

    return jsonify({"message":"book deleted"}), 200