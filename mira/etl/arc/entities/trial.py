import json

from sqlalchemy.orm import Session

from db.models import models
from db.schemas import core

def load_trial(db: Session, roc_graph):
    trial = models.Trial(
        trialDbId=roc_graph['./']['identifier'],
        trialName=roc_graph['./']['name'],
        datasetAuthorships = json.dumps([core.Dataset(
            # TODO: Implement
            # submissionDate=isa_json['submissionDate'],
            # publicReleaseDate=isa_json['publicReleaseDate'],
            license=roc_graph['./']['license'],        
        ).model_dump()]),
    )
    db.add(trial)
    db.commit()