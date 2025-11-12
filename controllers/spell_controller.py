from flask import jsonify, request

from db import db
from models.spell import Spells

def add_spell():
    post_data = request.form if request.form else request.get_json()

    fields = ['spell_name', 'incantation', 'difficulty_level', 'spell_type', 'description']
    required_fields =['spell_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_spell = Spells(values['spell_name'], values['incantation'], values['difficulty_level'], values['spell_type'], values['description']) 

    try:
        db.session.add(new_spell)
        db.session.commit()
    except: 
        db.session.rollback()
        return jsonify({"message": "unable to create record."}), 400 

    query = db.session.query(Spells).filter(Spells.spell_name == values['spell_name']).first()

    spell = {
        
        "spell_name": query.spell_name,
        "incantation": query.incantation,
        "difficulty_level": query.difficulty_level,
        "spell_type":query.spell_type,
        "description":query.description
    }

    return jsonify({"message":"spell created", "result":spell}), 201

# ===========================

def get_all_Spells():
    query = db.session.query(Spells).all()

    spell_list = []

    for spell in query:
        spell_dict = {
        "spell_id" : spell.spell_id,
        "spell_name": spell.spell_name,
        "incantation": spell.incantation,
        "difficulty_level": spell.difficulty_level,
        "spell_type":spell.spell_type,
        "description":spell.description
        }
        spell_list.append(spell_dict)

    return jsonify({"message": "spells founded.", "results": spell_list}), 200

# ============================

def get_spells_by_difficulty_level(difficulty_level):
    query= db.session.query(Spells).filter(Spells.difficulty_level == difficulty_level).all()
    if not query:
        return jsonify({"message": "no spells found with provided difficulty level"}), 404
    
    spell_difficulty_list = []

    for spell in query:
        spell_difficulty_dict = {
        "spell_id" : spell.spell_id,
        "spell_name": spell.spell_name,
        "incantation": spell.incantation,
        "difficulty_level": spell.difficulty_level,
        "spell_type":spell.spell_type,
        "description":spell.description
        }
        spell_difficulty_list.append(spell_difficulty_dict)

    return jsonify({"message":"spell found", "result": spell_difficulty_list}), 200

# ===============================

def update_spell_by_id(spell_id):
    post_data = request.form if request.form else request.get_json()
    spell_query = db.session.query(Spells).filter(Spells.spell_id==spell_id).first()

    if not spell_query:
        return jsonify({"message": "spell not found"}), 404

    spell_query.spell_name = post_data.get("spell_name", spell_query.spell_name)
    spell_query.incantation = post_data.get("incantation", spell_query.incantation)
    spell_query.difficulty_level = post_data.get("difficulty_level", spell_query.difficulty_level)
    spell_query.spell_type = post_data.get("spell_type", spell_query.spell_type)
    spell_query.description = post_data.get("description", spell_query.description)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}),400

    
    update_spell_query = db.session.query(Spells).filter(Spells.spell_id==spell_id).first()

    spell={
        "spell_id" : update_spell_query.spell_id,
        "spell_name": update_spell_query.spell_name,
        "incantation": update_spell_query.incantation,
        "difficulty_level": update_spell_query.difficulty_level,
        "spell_type":update_spell_query.spell_type,
        "description":update_spell_query.description
    }

    return jsonify ({"message": "record updated.", "result": spell}), 200

# ===============================

def delete_spell_by_id(spell_id):
    query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not query:
        return jsonify({"message": "spell not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete spell"}), 400

    return jsonify({"message":"spell deleted"}), 200