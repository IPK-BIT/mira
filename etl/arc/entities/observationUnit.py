from sqlalchemy.orm import Session
from db.models import models

def load_observationUnit(db: Session, o, context):
    observationUnit = models.ObservationUnit(
        observationUnitDbId=o['name'],
        germplasmDbId=context['germplasmDbId'],
        studyDbId=context['studyDbId'],
        trialDbId=context['trialDbId'],
        trialName=context['trialName'],
    )
    if db.get(models.ObservationUnit, o['name']) is None:
        db.add(observationUnit)
        db.commit()