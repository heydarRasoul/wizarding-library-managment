from flask import jsonify, request

from db import db
from models.wizard import Wizards
from models.school import Schools
from models.spell import Spells
from models.wizard_specializations import WizardSpecialization

def add_wizard():
    post_data = request.form if request.form else request.get_json()

    fields = ['school_id', 'wizard_name', 'house', 'year_enrolled', 'magical_power_level', 'active']
    required_fields =['school_id', 'wizard_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_wizard = Wizards(values['school_id'], values['wizard_name'], values['house'], values['year_enrolled'], values['magical_power_level'],values['active']) 

    try:
        db.session.add(new_wizard)
        db.session.commit()
    except: 
        db.session.rollback()
        return jsonify({"message": "unable to create record."}), 400 

    query = db.session.query(Wizards).filter(Wizards.wizard_name == values['wizard_name']).first()

    wizard_list = []

    school = db.session.query(Schools).filter(Schools.school_id == query.school_id).first()
    school_dict = {
        "school_id": school.school_id,
        "school_name": school.school_name,
        "location": school.location,
        "founded_year": school.founded_year,
        "headmaster": school.headmaster
    }
    
    specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == query.wizard_id).all()

    spells_list = []
    for spell in specializations:
        spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
        
        spell_dict = {
            "spell_id": spell_q.spell_id,
            "spell_name": spell_q.spell_name,
            "incantation": spell_q.incantation,
            "difficulty_level": spell_q.difficulty_level,
            "spell_type": spell_q.spell_type,
            "description": spell_q.description
        }

        specialization_dict = {
            "spell": spell_dict,
            "proficiency_level": spell.proficiency_level,
            "date_learned": spell.date_learned
        }
        spells_list.append(specialization_dict)


    wizard_dict = {
    "wizard_id" : query.wizard_id,
    "wizard_name": query.wizard_name,
    "house": query.house,
    "year_enrolled": query.year_enrolled,
    "magical_power_level":query.magical_power_level,
    "active":query.active,
    "school":school_dict,
    "spell":spells_list
    }
    wizard_list.append(wizard_dict)

    return jsonify({"message": "wizards created.", "result": wizard_list}), 200

# ===========================

def get_all_wizards():
    query = db.session.query(Wizards).all()
    

    wizard_list = []

    for wizard in query:
        school = db.session.query(Schools).filter(Schools.school_id == wizard.school_id).first()
        school_dict = {
            "school_id": school.school_id,
            "school_name": school.school_name,
            "location": school.location,
            "founded_year": school.founded_year,
            "headmaster": school.headmaster
        }

        specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == wizard.wizard_id).all()

        spells_list = []
        for spell in specializations:
            spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
           
            spell_dict = {
                "spell_id": spell_q.spell_id,
                "spell_name": spell_q.spell_name,
                "incantation": spell_q.incantation,
                "difficulty_level": spell_q.difficulty_level,
                "spell_type": spell_q.spell_type,
                "description": spell_q.description
            }

            specialization_dict = {
                "spell": spell_dict,
                "proficiency_level": spell.proficiency_level,
                "date_learned": spell.date_learned
            }
            spells_list.append(specialization_dict)


        wizard_dict = {
        "wizard_id" : wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level":wizard.magical_power_level,
        "active":wizard.active,
        "school":school_dict,
        "spell":spells_list
        }
        wizard_list.append(wizard_dict)

    return jsonify({"message": "wizards founded.", "results": wizard_list}), 200

# ============================

def get_wizard_by_id(wizard_id):
    query= db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()
    if not query:
        return jsonify({"message": "wizard has not found"}), 404
    
    wizard_list = []

    school = db.session.query(Schools).filter(Schools.school_id == query.school_id).first()
    school_dict = {
        "school_id": school.school_id,
        "school_name": school.school_name,
        "location": school.location,
        "founded_year": school.founded_year,
        "headmaster": school.headmaster
    }
    
    specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == query.wizard_id).all()

    spells_list = []
    for spell in specializations:
        spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
        
        spell_dict = {
            "spell_id": spell_q.spell_id,
            "spell_name": spell_q.spell_name,
            "incantation": spell_q.incantation,
            "difficulty_level": spell_q.difficulty_level,
            "spell_type": spell_q.spell_type,
            "description": spell_q.description
        }

        specialization_dict = {
            "spell": spell_dict,
            "proficiency_level": spell.proficiency_level,
            "date_learned": spell.date_learned
        }
        spells_list.append(specialization_dict)


    wizard_dict = {
    "wizard_id" : query.wizard_id,
    "wizard_name": query.wizard_name,
    "house": query.house,
    "year_enrolled": query.year_enrolled,
    "magical_power_level":query.magical_power_level,
    "active":query.active,
    "school":school_dict,
    "spell":spells_list
    }
    wizard_list.append(wizard_dict)

    return jsonify({"message": "wizards founded.", "results": wizard_list}), 200

# ===============================

def get_active_wizards():
    query = db.session.query(Wizards).filter(Wizards.active).all()
    if not query:
        return jsonify({"message": "no active wizard found"}), 404
    

    active_wizard_list = []

    for wizard in query:
        school = db.session.query(Schools).filter(Schools.school_id == wizard.school_id).first()
        school_dict = {
            "school_id": school.school_id,
            "school_name": school.school_name,
            "location": school.location,
            "founded_year": school.founded_year,
            "headmaster": school.headmaster
        }

        specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == wizard.wizard_id).all()

        spells_list = []
        for spell in specializations:
            spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
           
            spell_dict = {
                "spell_id": spell_q.spell_id,
                "spell_name": spell_q.spell_name,
                "incantation": spell_q.incantation,
                "difficulty_level": spell_q.difficulty_level,
                "spell_type": spell_q.spell_type,
                "description": spell_q.description
            }

            specialization_dict = {
                "spell": spell_dict,
                "proficiency_level": spell.proficiency_level,
                "date_learned": spell.date_learned
            }
            spells_list.append(specialization_dict)


        wizard_dict = {
        "wizard_id" : wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level":wizard.magical_power_level,
        "active":wizard.active,
        "school":school_dict,
        "spell":spells_list
        }
        active_wizard_list.append(wizard_dict)

    return jsonify({"message": "wizard founded.", "result": active_wizard_list}), 200

    
# ==============

def get_wizards_in_house(house):
    query = db.session.query(Wizards).filter(Wizards.house == house).all()
    if not query:
        return jsonify({"message": "no wizard founded with the house provided."}), 404
    

    wizards_in_house_list = []

    for wizard in query:
        school = db.session.query(Schools).filter(Schools.school_id == wizard.school_id).first()
        school_dict = {
            "school_id": school.school_id,
            "school_name": school.school_name,
            "location": school.location,
            "founded_year": school.founded_year,
            "headmaster": school.headmaster
        }

        specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == wizard.wizard_id).all()

        spells_list = []
        for spell in specializations:
            spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
           
            spell_dict = {
                "spell_id": spell_q.spell_id,
                "spell_name": spell_q.spell_name,
                "incantation": spell_q.incantation,
                "difficulty_level": spell_q.difficulty_level,
                "spell_type": spell_q.spell_type,
                "description": spell_q.description
            }

            specialization_dict = {
                "spell": spell_dict,
                "proficiency_level": spell.proficiency_level,
                "date_learned": spell.date_learned
            }
            spells_list.append(specialization_dict)


        wizard_dict = {
        "wizard_id" : wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level":wizard.magical_power_level,
        "active":wizard.active,
        "school":school_dict,
        "spell":spells_list
        }
        wizards_in_house_list.append(wizard_dict)

    return jsonify({"message": "wizards founded.", "results": wizards_in_house_list}), 200

# ============================

def get_wizards_magical_power_level(magical_power_level):
    query = db.session.query(Wizards).filter(Wizards.magical_power_level == int(magical_power_level)).all()
    if not query:
        return jsonify({"message": "no wizard founded with the magical power level provided"}), 404


    wizards_magical_power_level_list = []

    for wizard in query:
        school = db.session.query(Schools).filter(Schools.school_id == wizard.school_id).first()
        school_dict = {
            "school_id": school.school_id,
            "school_name": school.school_name,
            "location": school.location,
            "founded_year": school.founded_year,
            "headmaster": school.headmaster
        }

        specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == wizard.wizard_id).all()

        spells_list = []
        for spell in specializations:
            spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
           
            spell_dict = {
                "spell_id": spell_q.spell_id,
                "spell_name": spell_q.spell_name,
                "incantation": spell_q.incantation,
                "difficulty_level": spell_q.difficulty_level,
                "spell_type": spell_q.spell_type,
                "description": spell_q.description
            }

            specialization_dict = {
                "spell": spell_dict,
                "proficiency_level": spell.proficiency_level,
                "date_learned": spell.date_learned
            }
            spells_list.append(specialization_dict)


        wizard_dict = {
        "wizard_id" : wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level":wizard.magical_power_level,
        "active":wizard.active,
        "school":school_dict,
        "spell":spells_list
        }
        wizards_magical_power_level_list.append(wizard_dict)

    return jsonify({"message": "wizards founded.", "results": wizards_magical_power_level_list}), 200 


# ===========================

def update_wizard_by_id(wizard_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Wizards).filter(Wizards.wizard_id==wizard_id).first()

    if not query:
        return jsonify({"message": "wizard not found"}), 404

    query.wizard_name = post_data.get("wizard_name", query.wizard_name)
    query.house = post_data.get("house", query.house)
    query.year_enrolled = post_data.get("year_enrolled", query.year_enrolled)
    query.magical_power_level = post_data.get("magical_power_level", query.magical_power_level)
    query.active = post_data.get("active", query.active)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}),400

    wizard_list = []

    school = db.session.query(Schools).filter(Schools.school_id == query.school_id).first()
    school_dict = {
        "school_id": school.school_id,
        "school_name": school.school_name,
        "location": school.location,
        "founded_year": school.founded_year,
        "headmaster": school.headmaster
    }
    
    specializations = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == query.wizard_id).all()

    spells_list = []
    for spell in specializations:
        spell_q = db.session.query(Spells).filter(Spells.spell_id == spell.spell_id).first()
        
        spell_dict = {
            "spell_id": spell_q.spell_id,
            "spell_name": spell_q.spell_name,
            "incantation": spell_q.incantation,
            "difficulty_level": spell_q.difficulty_level,
            "spell_type": spell_q.spell_type,
            "description": spell_q.description
        }

        specialization_dict = {
            "spell": spell_dict,
            "proficiency_level": spell.proficiency_level,
            "date_learned": spell.date_learned
        }
        spells_list.append(specialization_dict)


    wizard_dict = {
    "wizard_id" : query.wizard_id,
    "wizard_name": query.wizard_name,
    "house": query.house,
    "year_enrolled": query.year_enrolled,
    "magical_power_level":query.magical_power_level,
    "active":query.active,
    "school":school_dict,
    "spell":spells_list
    }
    wizard_list.append(wizard_dict)

    return jsonify({"message": "record updated.", "result": wizard_list}), 200
   
# ===============================

def delete_wizard_by_id(wizard_id):
    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete wizard"}), 400

    return jsonify({"message":"wizard deleted"}), 200