from db.models import models
from sqlalchemy.orm import Session

def load_germplasm(db: Session, g, context):
    if db.get(models.Germplasm, g['name']):
        return
    genus=''
    species=''
    subtaxa=''
    seedSourceDescription = ''
    germplasmPUI = None
    germplasmCoordinates = {}
    for characteristic in g['characteristics']:
        if characteristic['category']['characteristicType']['annotationValue'] == 'Genus':
            genus = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Species':
            species = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Infraspecific Name':
            subtaxa = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Material source description':
            seedSourceDescription = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Material source DOI':
            germplasmPUI = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Material source latitude':
            germplasmCoordinates['latitude'] = characteristic['value']['annotationValue']
        elif characteristic['category']['characteristicType']['annotationValue'] == 'Material source longitude':
            germplasmCoordinates['longitude'] = characteristic['value']['annotationValue']
    germplasmOrigin = None
    if germplasmCoordinates['latitude']!='' and germplasmCoordinates['longitude']!='':
        germplasmOrigin = [{
            'coordinateUncertainty': None,
            'coordinates': {
                'geometry': {
                    'coordinates': [germplasmCoordinates['latitude'], germplasmCoordinates['longitude']],
                    'type': 'Point'
                },
                'type': 'Feature'
            }
        }]
    
    germplasm = models.Germplasm(
        germplasmDbId=g['name'],
        genus=genus,
        species=species,
        subtaxa=subtaxa,
        seedSourceDescription=seedSourceDescription,
        germplasmPUI=germplasmPUI,
        germplasmOrigin=germplasmOrigin
    )
    db.add(germplasm)
    db.commit()