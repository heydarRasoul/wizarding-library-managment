from flask import jsonify, request

from db import db
from models.wizard_specializations import WizardSpecialization

def add_wizard_specialization():
    post_data = request.form if request.form else request.get_json()

    fields = ['wizard_id', 'spell_id','proficiency_level', 'date_learned']
    required_fields =['wizard_id', 'spell_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_wizard_specialization = WizardSpecialization(values['wizard_id'], values['spell_id'], values['proficiency_level'], values['date_learned']) 

    try:
        db.session.add(new_wizard_specialization)
        db.session.commit()
    except: 
        db.session.rollback()
        return jsonify({"message": "unable to create record."}), 400 

    query = db.session.query(WizardSpecialization).filter(WizardSpecialization.wizard_id == values['wizard_id']).first()

    wizard_specialization = {
        "wizard_id" : query.wizard_id,
        "spell_id": query.spell_id,
        "proficiency_level": query.proficiency_level,
        "date_learned": query.date_learned
    }

    return jsonify({"message":"wizard-specialization created", "result":wizard_specialization}), 201
