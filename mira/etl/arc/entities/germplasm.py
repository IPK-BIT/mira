from db.models import models
from sqlalchemy.orm import Session

def load_germplasm(db: Session, germplasm_id, graph):
    if db.get(models.Germplasm, graph[germplasm_id]['name']):
        print(f"Germplasm {graph[germplasm_id]['name']} already exists in the database.")
        return
    
    ###
    # http://purl.obolibrary.org/obo/MIAPPE_0041 Organism
    # http://purl.obolibrary.org/obo/MIAPPE_0042 Genus
    # http://purl.obolibrary.org/obo/MIAPPE_0043 Species
    # http://purl.obolibrary.org/obo/MIAPPE_0044 Infraspecific name
    # http://purl.obolibrary.org/obo/MIAPPE_0045 Biological material latitude
    # http://purl.obolibrary.org/obo/MIAPPE_0046 Biological material longitude
    # http://purl.obolibrary.org/obo/MIAPPE_0047 Biological material altitude
    # http://purl.obolibrary.org/obo/MIAPPE_0048 Biological material coordinates uncertainty
    # http://purl.obolibrary.org/obo/MIAPPE_0049 Biological material preprocessing
    # http://purl.obolibrary.org/obo/MIAPPE_0050 Material source ID (Holding institute/stock centre, accession)
    # http://purl.obolibrary.org/obo/MIAPPE_0051 Material source DOI
    # http://purl.obolibrary.org/obo/MIAPPE_0052 Material source latitude
    # http://purl.obolibrary.org/obo/MIAPPE_0053 Material source longitude
    # http://purl.obolibrary.org/obo/MIAPPE_0054 Material source altitude
    # http://purl.obolibrary.org/obo/MIAPPE_0055 Material source coordinates uncertainty
    # http://purl.obolibrary.org/obo/MIAPPE_0056 Material source description
    ###    
    genus=None
    species=None
    subtaxa=None
    germplasmPui=None
    seedSourceDescription=None
    longitude=None
    latitude=None
    coordinatesUncertainty=None
    for prop in [graph[node['@id']] for node in graph[germplasm_id]['additionalProperty']]:
        genus = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0042' else genus
        species = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0043' else species
        subtaxa = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0044' else subtaxa
        germplasmPui = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0051' else germplasmPui
        seedSourceDescription = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0056' else seedSourceDescription
        latitude = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0052' else latitude
        longitude = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0053' else longitude
        coordinatesUncertainty = prop.get('value') if prop['propertyID'] == 'http://purl.obolibrary.org/obo/MIAPPE_0055' else coordinatesUncertainty
    germplasmOrigin = None
    if longitude and latitude:
        germplasmOrigin = [{
            'coordinatesUncertainty': coordinatesUncertainty,
            'coordinates': {
                'geometry':{
                    'coordinates': [longitude, latitude],
                    'type': 'Point'
                },
                'type': 'Feature'
            }
        }]
    
    germplasm = models.Germplasm(
        germplasmDbId=graph[germplasm_id]['name'],
        germplasmName=graph[germplasm_id]['name'],
        genus=genus,
        species=species,
        subtaxa=subtaxa,
        germplasmPUI=germplasmPui,
        seedSourceDescription=seedSourceDescription,
        germplasmOrigin=germplasmOrigin,
    )
    
    db.add(germplasm)
    db.commit()