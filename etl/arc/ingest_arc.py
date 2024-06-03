import json
import os
from arctrl.arctrl import JsonController
from arctrl.arc import ARC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from etl.arc.entities.study import load_study
from etl.arc.entities.trial import load_trial
from etl.arc.entities.germplasm import load_germplasm
from etl.arc.entities.observationUnit import load_observationUnit
from etl.arc.entities.variable import load_variables
from etl.arc.entities.observation import load_observations

DATA_DIR = 'data/rocrate/'
DATABASE_URL = 'sqlite:///miappe.db'

def extract(data_dir: str = DATA_DIR):
    jsonString = open(os.path.join(data_dir, 'metadata.json')).read()

    return JsonController.ARC().from_rocrate_json_string(jsonString)

def transform_and_load(data: ARC, data_dir: str = DATA_DIR):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    isa_json= json.loads(JsonController.Investigation().to_isajson_string(data.ISA))

    load_trial(db, isa_json)

    for s in isa_json['studies']:
        load_study(db, s, isa_json)       
        growth_process = next((process for process in s['processSequence'] if process['name'] == 'Growth'), None)
        for input in growth_process['inputs']:
            load_germplasm(db, input, None)
        for i in range(0, len(growth_process['outputs'])):
            output = growth_process['outputs'][i]
            context = {
                'trialDbId': isa_json['identifier'],
                'trialName': isa_json['title'],
                'studyDbId': s['identifier'],
                'studyName': s['title'],
                'germplasmDbId': growth_process['inputs'][i]['name']
            }
            load_observationUnit(db, output, context)
        
        load_variables(db, os.path.join(data_dir, os.path.dirname(s['filename']), 'tdf.tsv').replace('assays', 'studies'))
        
        for a in s['assays']:
            for process in a['processSequence']:
                if process['name'] == 'Phenotyping':
                    data_files = [x for i, x in enumerate(process['outputs']) if x['name'] not in [y['name'] for y in process['outputs'][:i]]]
                    for data_file in data_files:
                        load_observations(db, os.path.join(data_dir, os.path.dirname(a['filename']), 'datasets', data_file['name']), context={"study": s, "assay": a})

    db.close()
