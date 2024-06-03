from icecream import ic
import json
from uuid import uuid4
import polars as pl
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from litestar.datastructures import State

from db.models import models
from db.schemas import phenotyping, commons

DATA_DIR = 'data/isatab/'
DATABASE_URL = 'sqlite:///miappe.db'

def extract(): 
    check_dataset()
    data = {'investigation': read_investigation(), 'studies': [], 'assays': [], 'data': []}
    for study_file in data['investigation']['Study File Name']:
        data['studies'].append(pl.read_csv(os.path.join(DATA_DIR, study_file), separator='\t'))
    for assay_file in data['investigation']['Study Assay File Name']:
        data['assays'].append(pl.read_csv(os.path.join(DATA_DIR, assay_file), separator='\t'))
    for data_file in data['investigation']['Comment[Study Data File Link]']:
        data['data'].append(pl.read_csv(os.path.join(DATA_DIR, data_file), separator='\t'))
    for trait_file in data['investigation']['Comment[Trait Definition File]']:
        data['traits']=pl.read_csv(os.path.join(DATA_DIR, trait_file), separator='\t')
    return data

def transform_and_load(data):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    for miappe_trait in data['traits'].iter_rows(named=True):
        method = phenotyping.Method(
            methodName=miappe_trait['Method'],
            methodDbId=miappe_trait['Method Accession Number'],
        )
        valueRange = None,
        unit = None
        if miappe_trait['Scale Type'] in ['Nominal', 'Ordinal']:
            valueRange = commons.ScaleValues(
                categories=[]
            )
            for value in miappe_trait['Method Description'].split(','):
                annotation = value.split(':')
                valueRange.categories.append(commons.ScaleValue(
                    value=annotation[0],
                    label=annotation[1][1:-1]
                ))
            scale = phenotyping.Scale(
                scaleName=miappe_trait['Scale'],
                scaleDbId=miappe_trait['Scale Accession Number'],
                validValues=valueRange,
            )
        elif miappe_trait['Scale Type'] == 'Numerical':
            unit = miappe_trait['Method Description']
            scale = phenotyping.Scale(
                scaleName=miappe_trait['Scale'],
                scaleDbId=miappe_trait['Scale Accession Number'],
                units=unit,
            )
        trait = phenotyping.Trait(
            traitName=miappe_trait['Trait'],
            traitDbId=miappe_trait['Trait Accession Number'],
        )
        variable = models.ObservationVariable(
            observationVariableDbId=miappe_trait['Variable ID'],
            observationVariableName=miappe_trait['Variable Name'],
            observationVariablePUI=miappe_trait['Variable Accession Number'],
            method=json.dumps(method.model_dump()),
            scale=scale.model_dump(),
            trait=json.dumps(trait.model_dump())
        )
        db.add(variable)

    db.commit()
    db.close()
    
    result = {'observedVariables': []}
    return result

def check_dataset():
    """
    Check the dataset for the presence of the necessary files. 
    """
    i_file = read_investigation()

    if len(i_file['Study File Name'])!=len(i_file['Study Assay File Name']) and len(i_file['Study File Name'])!=len(i_file['Comment[Study Data File Link]']):
        raise Exception('Study files, assay files and data files should have the same number.')

    for study_file in i_file['Study File Name']:
        if not os.path.exists(os.path.join(DATA_DIR, study_file)):
            raise Exception(f'Study file {study_file} not found.')

    for assay_file in i_file['Study Assay File Name']:
        if not os.path.exists(os.path.join(DATA_DIR, assay_file)):
            raise Exception(f'Assay file {assay_file} not found.')

    for data_file in i_file['Comment[Study Data File Link]']:
        if not os.path.exists(os.path.join(DATA_DIR, data_file)):
            raise Exception(f'Data file {data_file} not found.')
        
    if not os.path.exists(os.path.join(DATA_DIR, i_file['Comment[Trait Definition File]'][0])):
        raise Exception(f'Trait definition file not found.')

    return i_file

def read_investigation():
    investigation_file = None
    for file in os.listdir(DATA_DIR):
        if file.startswith('i_'):
            investigation_file = file
            break
    if not investigation_file:
        raise Exception('No investigation file found on top level.')
    i_file = {}
    with open(os.path.join(DATA_DIR, investigation_file)) as fp:
        lines = fp.readlines()
        for line in lines:
            tmp = line.strip().split('\t')
            if len(tmp)>1:
                    i_file[tmp[0]] = tmp[1:]
    return i_file