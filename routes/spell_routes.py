from flask import Blueprint
import controllers

spell = Blueprint('spell', __name__)

@spell.route ('/spell', methods=['POST'])
def add_spell_route():
    return controllers.add_spell()

@spell.route('/spells', methods=['GET'])
def get_all_spells_route():
    return controllers.get_all_Spells()

@spell.route('/spells/<difficulty_level>' , methods=['GET'])
def get_spells_by_difficulty_level_route(difficulty_level):
    return controllers.get_spells_by_difficulty_level(difficulty_level)

@spell.route('/spell/<spell_id>', methods=['PUT'])
def update_spell_by_id_route(spell_id):
    return controllers.update_spell_by_id(spell_id)

@spell.route('/spell/delete/<spell_id>', methods=['DELETE'])
def delete_spell_by_id_route(spell_id):
    return controllers.delete_spell_by_id(spell_id)
