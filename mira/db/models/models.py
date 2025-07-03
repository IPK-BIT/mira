import json
from typing import Any

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.types import TypeDecorator

SIZE = 256
class JSONType(TypeDecorator):
    impl = sqlalchemy.Text(SIZE)
    def process_bind_param(self, value: Any | None, dialect: sqlalchemy.Dialect) -> sqlalchemy.Any:
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value: Any | None, dialect: sqlalchemy.Dialect) -> Any | None:
        if value is not None:
            value = json.loads(value)
        return value
    
class Base(DeclarativeBase):
    ...

class Trial(Base):
    __tablename__ = 'trials'

    active: Mapped[bool|None]
    additionalInfo = sqlalchemy.Column(JSONType)
    commonCropName: Mapped[str|None]
    contacts = sqlalchemy.Column(JSONType)
    datasetAuthorships = sqlalchemy.Column(JSONType)
    documentationURL: Mapped[str|None]
    endDate: Mapped[str|None]
    externalReferences = sqlalchemy.Column(JSONType)
    programDbId: Mapped[str|None]
    programName: Mapped[str|None]
    publications = sqlalchemy.Column(JSONType)
    startDate: Mapped[str|None]
    trialDbId: Mapped[str] = mapped_column(primary_key=True)
    trialDescription: Mapped[str|None]
    trialName: Mapped[str|None]
    trialPUI: Mapped[str|None]

class Study(Base):
    __tablename__ = 'studies'

    active: Mapped[bool|None]
    additionalInfo = sqlalchemy.Column(JSONType)
    commonCropName: Mapped[str|None]
    contacts = sqlalchemy.Column(JSONType)
    culturalPractices: Mapped[str|None]
    dataLinks = sqlalchemy.Column(JSONType)
    documentationURL: Mapped[str|None]
    endDate: Mapped[str|None]
    environmentParameters = sqlalchemy.Column(JSONType)
    experimentalDesign = sqlalchemy.Column(JSONType)
    externalReferences = sqlalchemy.Column(JSONType)
    growthFacility: Mapped[str|None]
    lastUpdate = sqlalchemy.Column(JSONType)
    license: Mapped[str|None]
    locationDbId: Mapped[str|None]
    locationName: Mapped[str|None]
    observationLevels = sqlalchemy.Column(JSONType)
    observationUnitsDescription: Mapped[str|None]
    observationVariableDbIds = sqlalchemy.Column(JSONType)
    season = sqlalchemy.Column(JSONType)
    startDate: Mapped[str|None]
    studyDbId: Mapped[str] = mapped_column(primary_key=True)
    studyDescription: Mapped[str|None]
    studyName: Mapped[str|None]
    studyPUI: Mapped[str|None]
    studyType: Mapped[str|None]
    trialDbId: Mapped[str|None]
    trialName: Mapped[str|None]

class Germplasm(Base):
    __tablename__ = 'germplasms'
    
    accessionNumber: Mapped[str|None]
    acquisitionDate: Mapped[str|None]
    additionalInfo = sqlalchemy.Column(JSONType)
    biologicalStatusOfAccessionCode: Mapped[str|None]
    biologicalStatusOfAccessionDescription: Mapped[str|None]
    breedingMethodDbId: Mapped[str|None]
    breedingMethodDescription: Mapped[str|None]
    collection: Mapped[str|None]
    commonCropName: Mapped[str|None]
    countryOfOriginCode: Mapped[str|None]
    defaultDisplayName: Mapped[str|None]
    documentationURL: Mapped[str|None]
    donors = sqlalchemy.Column(JSONType)
    genus: Mapped[str|None]
    germplasmDbId: Mapped[str] = mapped_column(primary_key=True)
    germplasmName: Mapped[str|None]
    germplasmOrigin = sqlalchemy.Column(JSONType)
    germplasmPUI: Mapped[str|None]
    germplasmPreprocessing: Mapped[str|None]
    instituteCode: Mapped[str|None]
    instituteName: Mapped[str|None]
    pedigree: Mapped[str|None]
    seedSource: Mapped[str|None]
    seedSourceDescription: Mapped[str|None]
    species: Mapped[str|None]
    storageTypes = sqlalchemy.Column(JSONType)
    subtaxa: Mapped[str|None]
    subtaxaAuthority: Mapped[str|None]
    synonyms = sqlalchemy.Column(JSONType)
    taxonIds = sqlalchemy.Column(JSONType)

class ObservationUnit(Base):
    __tablename__ = 'observation_units'
    
    additionalInfo = sqlalchemy.Column(JSONType)
    crossDbId: Mapped[str|None]
    crossName: Mapped[str|None]
    externalReferences = sqlalchemy.Column(JSONType)
    germplasmDbId: Mapped[str|None]
    germplasmName: Mapped[str|None]
    locationDbId: Mapped[str|None]
    locationName: Mapped[str|None]
    observationUnitDbId: Mapped[str] = mapped_column(primary_key=True)
    observationUnitName: Mapped[str|None]
    observationUnitPUI: Mapped[str|None]
    observationUnitPosition = sqlalchemy.Column(JSONType)
    observations = sqlalchemy.Column(JSONType)
    programDbId: Mapped[str|None]
    programName: Mapped[str|None]
    seedLotDbId: Mapped[str|None]
    seedLotName: Mapped[str|None]
    studyDbId: Mapped[str|None]
    studyName: Mapped[str|None]
    treatments = sqlalchemy.Column(JSONType)
    trialDbId: Mapped[str|None]
    trialName: Mapped[str|None]

class ObservationVariable(Base):
    __tablename__ = 'observation_variables'
    
    additionalInfo = sqlalchemy.Column(JSONType)
    commonCropName: Mapped[str|None]
    contextOfUse = sqlalchemy.Column(JSONType)
    defaultValue: Mapped[str|None]
    documentationURL: Mapped[str|None]
    externalReferences = sqlalchemy.Column(JSONType)
    growthStage: Mapped[str|None]
    institution: Mapped[str|None]
    language: Mapped[str|None]
    method = sqlalchemy.Column(JSONType)
    observationVariableDbId: Mapped[str] = mapped_column(primary_key=True)
    observationVariableName: Mapped[str|None]
    observationVariablePUI: Mapped[str|None]
    ontologyReference = sqlalchemy.Column(JSONType)
    scale = sqlalchemy.Column(JSONType)
    scientist: Mapped[str|None]
    status: Mapped[str|None]
    submissionTimestamp: Mapped[str|None]
    synonyms = sqlalchemy.Column(JSONType)
    trait = sqlalchemy.Column(JSONType)

class Observation(Base):
    __tablename__ = 'observations'

    additionalInfo = sqlalchemy.Column(JSONType)
    collector: Mapped[str|None]
    externalReferences = sqlalchemy.Column(JSONType)
    germplasmDbId: Mapped[str|None]
    germplasmName: Mapped[str|None]
    observationDbId: Mapped[str] = mapped_column(primary_key=True)
    observationTimeStamp: Mapped[str|None]
    observationUnitDbId: Mapped[str|None]
    observationUnitName: Mapped[str|None]
    observationVariableDbId: Mapped[str|None]
    observationVariableName: Mapped[str|None]
    season = sqlalchemy.Column(JSONType)
    studyDbId: Mapped[str|None]
    studyName: Mapped[str|None]
    uploadedBy: Mapped[str|None]
    value: Mapped[str|None]