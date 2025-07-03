from sqlalchemy.orm import Session
from db.models import models

def load_observationUnit(db: Session, observationunit_id, study_id, germplasm_id, graph):
    if db.get(models.ObservationUnit, graph[observationunit_id]['name']):
        print(f"Observation unit {graph[observationunit_id]['name']} already exists in the database.")
        return
    observationunit = models.ObservationUnit(
        observationUnitDbId=graph[observationunit_id]['name'],
        observationUnitName=graph[observationunit_id]['name'],
        germplasmDbId=graph[germplasm_id]['name'],
        germplasmName=graph[germplasm_id]['name'],
        studyDbId=graph[study_id]['identifier'],
        studyName=graph[study_id]['name'],
        trialDbId=graph['./']['identifier'],
        trialName=graph['./']['name'],
    )
    db.add(observationunit)
    db.commit()