from pydantic import BaseModel
#from typing import Optional

class Pagination(BaseModel):
    currentPage: int
    pageSize: int
    totalCount: int
    totalPages: int

class Status(BaseModel):
    message: str
    messageType: str

class Metadata(BaseModel):
    datafiles: list[str]
    pagination: Pagination
    status: list[Status]

class ExternalReference(BaseModel):
    referenceId: str|None
    referenceSource: str|None

class Geometry(BaseModel):
    coordinates: list[float|None]
    type: str

class GeoCoordinates(BaseModel):
    geometry: Geometry
    type: str

class Season(BaseModel):
    seasonDbId: str|None
    seasonName: str|None
    year: str|None

class Observation(BaseModel):
    additionalInfo: dict|None = None
    collector: str|None = None
    externalReferences: list[ExternalReference]|None = None
    geoCoordinates: GeoCoordinates|None = None
    germplasmDbId: str|None = None
    germplasmName: str|None = None
    observationDbId: str|None = None
    observationTimeStamp: str|None = None
    observationUnitDbId: str|None = None
    observationUnitName: str|None = None
    observationVariableDbId: str|None = None
    observationVariableName: str|None = None
    season: Season|None = None
    studyDbId: str|None = None
    uploadedBy: str|None = None
    value: str|None = None

class ObservationLevel(BaseModel):
    levelCode: str|None = None
    levelName: str|None = None
    levelOrder: str|None = None

class Treatment(BaseModel):
    factor: str|None = None
    modality: str|None = None

class ObservationUnitPosition(BaseModel):
    entryType: str|None = None
    geoCoordinates: GeoCoordinates|None = None
    observationLevel: ObservationLevel|None = None
    observationLevelRelationships: list[ObservationLevel]|None = None
    positionCoordinateX: str|None = None
    positionCoordinateXType: str|None = None
    positionCoordinateY: str|None = None
    positionCoordinateYType: str|None = None

class ObservationUnit(BaseModel):
    additionalInfo: dict|None = None
    crossDbId: str|None = None
    crossName: str|None = None
    externalReferences: list[ExternalReference]|None = None
    germplasmDbId: str|None = None
    germplasmName: str|None = None
    locationDbId: str|None = None
    locationName: str|None = None
    observationUnitDbId: str|None = None
    observationUnitName: str|None = None
    observationUnitPUI: str|None = None
    observationUnitPosition: ObservationUnitPosition|None = None
    observations: list[Observation]|None = None
    programDbId: str|None = None
    programName: str|None = None
    seedLotDbId: str|None = None
    seedLotName: str|None = None
    studyDbId: str|None = None
    studyName: str|None = None
    treatments: list[Treatment]|None = None
    trialDbId: str|None = None
    trialName: str|None = None

class OntologyAnnotation(BaseModel):
    URL: str|None = None
    type: str|None = None

class Ontology(BaseModel):
    documentationLinks: list[OntologyAnnotation]|None = None
    ontologyDbId: str|None = None
    ontologyName: str|None = None
    version: str|None = None

class Method(BaseModel):
    additionalInfo: dict|None = None
    bibliographicalReference: str|None = None
    description: str|None = None
    externalReferences: list[ExternalReference]|None = None
    formula: str|None = None
    methodClass: str|None = None
    methodDbId: str|None = None
    methodName: str|None = None
    methodPUI: str|None
    ontologyReference: Ontology|None

class ValueAnnotation(BaseModel):
    label: str|None
    value: str|None

class ValueRange(BaseModel):
    categories: list[ValueAnnotation]|None
    maximumValue: str|None
    minimumValue: str|None

class Trait(BaseModel):
    additionalInfo: dict|None
    alternativeAbbreviations: list[str]|None
    attribute: str|None
    attributePUI: str|None
    entity: str|None
    externalReferences: list[ExternalReference]|None
    mainAbbreviation: str|None
    ontologyReference: Ontology|None
    status: str|None
    synonyms: list[str]|None
    traitClass: str|None
    traitDbId: str|None
    traitDescription: str|None
    traitName: str|None
    traitPUI: str|None

class Scale(BaseModel):
    additionalInfo: dict|None
    dataType: str|None
    decimalPlaces: int|None
    externalReferences: list[ExternalReference]|None
    ontologyReference: Ontology|None
    scaleDbId: str|None
    scaleName: str|None
    scalePUI: str|None
    units: str|None
    validValues: ValueRange|None

class ObservationVariable(BaseModel):
    additionalInfo: dict|None
    commonCropName: str|None
    contextOfUse: list[str]|None
    defaultValue: str|None
    documentationURL: str|None
    externalReferences: list[ExternalReference]|None
    growthStage: str|None
    institution: str|None
    language: str|None
    method: Method|None
    observationVariableDbId: str|None
    observationVariableName: str|None
    observationVariablePUI: str|None
    ontologyReference: Ontology|None
    scale: Scale|None
    scientist: str|None
    status: str|None
    submissionTimestamp: str|None
    synonyms: list[str]|None
    trait: Trait|None

class Call(BaseModel):
    contentTypes: list[str]|None = None
    methods: list[str]|None = None
    service: str|None = None
    versions: list[str]|None = None

class ServerInfo(BaseModel):
    calls: list[Call]
    contactEmail: str|None
    documentationURL: str|None
    location: str|None
    organizationName: str|None
    organizationURL: str|None
    serverDescription: str|None
    serverName: str|None = None