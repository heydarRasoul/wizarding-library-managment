from flask import Blueprint
import controllers

wizard_specialization = Blueprint('wizard_specialization', __name__)

@wizard_specialization.route ('/wizard/specialize', methods=['POST'])
def add_wizard_specialization_route():
    return controllers.add_wizard_specialization()
