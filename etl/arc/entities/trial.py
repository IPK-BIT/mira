from icecream import ic

import json

from db.models import models
from db.schemas import core

from sqlalchemy.orm import Session

def load_trial(db: Session, isa_json):
    # ic(isa_json)
    trial = models.Trial(
        additionalInfo = {
            'MIAPPE-Version': next((comment['value'] for comment in isa_json['comments'] if comment['name'] == 'MIAPPE version'), None),
        },
        trialDbId = isa_json['identifier'],
        trialName = isa_json['title'],
        # trialDescription = isa_json['description'],
        datasetAuthorships = json.dumps([core.Dataset(
            # TODO: Implement
            # submissionDate=isa_json['submissionDate'],
            # publicReleaseDate=isa_json['publicReleaseDate'],
            license=next((comment['value'] for comment in isa_json['comments'] if comment['name'] == 'License'), None),        
        ).model_dump()]),
        #TODO: Implement publications
    )
    db.add(trial)
    db.commit()