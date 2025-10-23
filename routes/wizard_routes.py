from flask import Blueprint
import controllers

wizard = Blueprint('wizard', __name__)

@wizard.route ('/wizard', methods=['POST'])
def add_wizard_route():
    return controllers.add_wizard()


@wizard.route('/wizards', methods=['GET'])
def get_all_wizards_route():
    return controllers.get_all_wizards()

@wizard.route('/wizard/<wizard_id>' , methods=['GET'])
def get_wizard_by_id_route(wizard_id):
    return controllers.get_wizard_by_id(wizard_id)

@wizard.route('/wizards/active' , methods=['GET'])
def get_active_wizards_active():
    return controllers.get_active_wizards()

@wizard.route('/wizards/<house>' , methods=['GET'])
def get_wizards_in_house_route(house):
    return controllers.get_wizards_in_house(house)

@wizard.route('/wizards/magiclv/<magical_power_level>' , methods=['GET'])
def get_wizards_magical_power_level_route(magical_power_level):
    return controllers.get_wizards_magical_power_level(magical_power_level)

@wizard.route('/wizard/<wizard_id>', methods=['PUT'])
def update_wizard_by_id_route(wizard_id):
    return controllers.update_wizard_by_id(wizard_id)

@wizard.route('/wizard/delete/<wizard_id>', methods=['DELETE'])
def delete_wizard_by_id_route(wizard_id):
    return controllers.delete_wizard_by_id(wizard_id)
