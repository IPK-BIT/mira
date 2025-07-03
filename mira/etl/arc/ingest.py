import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from arctrl.arc import ARC
from arctrl.Contract.contract import Contract, DTO
from fsspreadsheet.xlsx import Xlsx
from pathlib import Path

from etl.arc.entities.trial import load_trial
from etl.arc.entities.study import load_study
from etl.arc.entities.germplasm import load_germplasm
from etl.arc.entities.observationunit import load_observationUnit
from etl.arc.entities.observationvariable import load_variables
from etl.arc.entities.observation import load_observations


def ingest(data_dir: str):
    engine = create_engine('sqlite:///miappe.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    arc_obj = read(data_dir)
    rocrate_json = json.loads(ARC.to_rocrate_json_string()(arc_obj))
    graph = {}
    for node in rocrate_json['@graph']:
        graph[node['@id']] = node

    load_trial(db, graph)
    for study in [node for node in graph['./']['hasPart'] if graph[node['@id']]['additionalType'] == 'Study']:
        load_study(db, study['@id'], graph)
        for process in [graph[node['@id']] for node in graph[study['@id']]['about'] if graph[graph[node['@id']]['executesLabProtocol']['@id']]['name']=='Growth']:
            load_germplasm(db, process['object']['@id'], graph)
            load_observationUnit(db, process['result']['@id'], study['@id'], process['object']['@id'], graph)
        load_variables(db, data_dir + '/' + study['@id'] + 'resources/tdf.tsv')
    
    for assay in [node for node in graph['./']['hasPart'] if graph[node['@id']]['additionalType'] == 'Assay']:
        for process in [graph[node['@id']] for node in graph[assay['@id']]['about'] if graph[graph[node['@id']]['executesLabProtocol']['@id']]['name']=='Phenotyping']:
            # Read the df filename from the assay
            load_observations(db, data_dir + '/' + assay['@id'] + 'dataset/df.tsv', process['@id'], graph)
            
            
def normalize_path_separators(path_str: str):
    normalized_path = os.path.normpath(path_str)
    return normalized_path.replace('//', '/')


def get_all_file_paths(base_path):
    files_list = []

    def loop(dir_path):
        files = os.listdir(dir_path)
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                loop(file_path)
            else:
                relative_path = os.path.relpath(file_path, base_path)
                normalize_path = normalize_path_separators(relative_path)
                files_list.append(normalize_path)
    loop(base_path)
    return files_list


def read(base_path):
    all_file_paths = get_all_file_paths(base_path)
    arc = ARC.from_file_paths(all_file_paths)
    read_contracts = arc.GetReadContracts()
    _ = [fulfill_read_contract(base_path, contract)
         for contract in read_contracts]
    arc.SetISAFromContracts(read_contracts)
    return arc

def fulfill_read_contract(basePath: str, contract: Contract):
    print("Fulfilling contract:", basePath, contract)
    if contract.Operation == "READ":
        normalizedPath = os.path.normpath(
            Path(basePath).joinpath(contract.Path))
        if contract.DTOType.name == "ISA_Assay" or contract.DTOType.name == "ISA_Study" or contract.DTOType.name == "ISA_Investigation":
            fswb = Xlsx.from_xlsx_file(normalizedPath)
            contract.DTO = DTO(0, fswb)
        elif contract.DTOType == "PlainText":
            content = Path.read_text(normalizedPath)
            contract.DTO = DTO(1, content)
        else:
            print(
                "Handling of ${contract.DTOType} in a READ contract is not yet implemented")

    else:
        print(
            "Error (fulfillReadContract): ${contract} is not a READ contract")