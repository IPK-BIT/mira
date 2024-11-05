import polars as pl
from sqlalchemy.orm import Session
from dateutil.parser import parse

from db.models.models import Observation

def load_observations(db: Session, filename, context):
    if (filename.endswith('.tsv')):
        df = pl.read_csv(filename, separator='\t')
    else:
        df = pl.read_csv(filename)
    for o in df.iter_rows(named=True):
        germplasmDbId = None
        for idx in range(0, len(context['study']['processSequence'][0]['outputs'])):
            if context['study']['processSequence'][0]['outputs'][idx]['name'] == o['Assay Name']:
                germplasmDbId = context['study']['processSequence'][0]['inputs'][idx]['name']
        
        try:
            study_title = context['study']['title']
        except KeyError:
            study_title = context['study']['identifier']
        observation = Observation(
            germplasmDbId=germplasmDbId,
            observationDbId=o['Assay Name']+'-'+o['Trait']+'-'+parse(o['Date']).strftime("%Y-%m-%dT%H:%M:%SZ"),
            observationUnitDbId=o['Assay Name'],
            observationTimeStamp=parse(o['Date']).strftime("%Y-%m-%dT%H:%M:%SZ"),
            observationVariableDbId=o['Trait'],
            studyDbId=context['study']['identifier'],
            studyName=study_title,
            value=str(o['Value'])
        )
        db.add(observation)
    db.commit()