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
        
    germplasm = models.Germplasm(
        germplasmDbId=g['name'],
        genus=genus,
        species=species,
        subtaxa=subtaxa,
        seedSourceDescription=seedSourceDescription,
        germplasmPUI=germplasmPUI
    )
    db.add(germplasm)
    db.commit()