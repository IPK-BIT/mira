from db.models import models
from sqlalchemy.orm import Session

def load_study(db: Session, study_id, graph):
    study = models.Study(
        studyDbId=graph[study_id]['identifier'],
        studyName=graph[study_id]['name'],
        trialDbId=graph['./']['identifier'],
        trialName=graph['./']['name'],
    )
    db.add(study)
    db.commit()