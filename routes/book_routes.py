from flask import Blueprint
import controllers

book = Blueprint('book', __name__)

@book.route ('/book', methods=['POST'])
def add_book_route():
    return controllers.add_book()

@book.route('/books', methods=['GET'])
def get_all_books_route():
    return controllers.get_all_books()

@book.route('/books/available' , methods=['GET'])
def get_available_Books():
    return get_available_Books()

@book.route('/book/<book_id>', methods=['PUT'])
def update_book_by_id_route(book_id):
    return controllers.update_book_by_id(book_id)

@book.route('/book/delete/<book_id>', methods=['DELETE'])
def delete_book_by_id_route(book_id):
    return controllers.delete_book_by_id(book_id)
