from db.models import models
from sqlalchemy.orm import Session

def load_study(db: Session, s, isa_json):
    study = models.Study(
            studyDbId = s['identifier'],
            studyName = s['title'],
            # TODO: add remaining properties
            # studyDescription='',
            # startDate='',
            # endDate='',
            # instituteName='',
            # FIXME: Location resemblance in Study seems to have changed 
            # locationName='',
            trialDbId=isa_json['identifier'],
            trialName=isa_json['title'],
        )
    db.add(study)
    db.commit()
