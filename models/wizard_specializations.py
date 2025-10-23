import uuid
from sqlalchemy.dialects.postgresql import UUID 

from db import db


class WizardSpecialization(db.Model):
    __tablename__="WizardSpecialization"


    wizard_id = db.Column(UUID(as_uuid=True),db.ForeignKey("Wizards.wizard_id"), primary_key=True, default=uuid.uuid4)
    spell_id = db.Column(UUID(as_uuid=True),db.ForeignKey("Spells.spell_id"), primary_key=True, default=uuid.uuid4)
    proficiency_level = db.Column(db.Float())
    date_learned = db.Column(db.DateTime)

    wizard = db.relationship("Wizards", back_populates="specializations")
    spell = db.relationship("Spells", back_populates="specializations")

    def __init__(self, wizard_id, spell_id,proficiency_level, date_learned):
        self.wizard_id=wizard_id
        self.spell_id=spell_id
        self.proficiency_level=proficiency_level
        self.date_learned=date_learned
