import polars as pl
from sqlalchemy.orm import Session
from dateutil.parser import parse

from db.models import models

def load_observations(db: Session, df: pl.DataFrame, process_id, graph):
    df = df.filter(pl.col("Assay Name") == graph[graph[process_id]['object']['@id']]['name'])

    for obs in df.iter_rows(named=True):
        db_variable=db.get(models.ObservationVariable, obs['Trait'])
        if not db_variable:
            print(obs['Trait'])
        db_observationunit = db.get(models.ObservationUnit, obs['Assay Name'])
        observation = models.Observation(
            observationUnitDbId=obs['Assay Name'],
            observationUnitName=db_observationunit.observationUnitName,
            observationDbId='-'.join([obs['Assay Name'], obs['Trait'], obs['Date']]),
            observationVariableDbId=obs['Trait'],
            observationVariableName=db_variable.observationVariableName,
            observationTimeStamp=parse(obs['Date']).isoformat(),
            studyDbId=db_observationunit.studyDbId,
            studyName=db_observationunit.studyName,
            germplasmDbId=db_observationunit.germplasmDbId,
            germplasmName=db_observationunit.germplasmName,
            value=str(obs['Value']),
        )
        db.add(observation)
    db.commit() 