from pydantic import BaseModel
from typing import Optional

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
    additionalInfo: dict|None
    collector: str|None
    externalReferences: list[ExternalReference]|None
    geoCoordinates: GeoCoordinates|None
    germplasmDbId: str|None
    germplasmName: str|None
    observationDbId: str|None
    observationTimeStamp: str|None
    observationUnitDbId: str|None
    observationUnitName: str|None
    observationVariableDbId: str|None
    observationVariableName: str|None
    season: Season|None
    studyDbId: str|None
    uploadedBy: str|None
    value: str|None

class ObservationLevel(BaseModel):
    levelCode: str|None
    levelName: str|None
    levelOrder: str|None

class Treatment(BaseModel):
    factor: str|None
    modality: str|None

class ObservationUnitPosition(BaseModel):
    entryType: str|None
    geoCoordinates: GeoCoordinates|None
    observationLevel: ObservationLevel|None
    observationLevelRelationships: list[ObservationLevel]|None
    positionCoordinateX: str|None
    positionCoordinateXType: str|None
    positionCoordinateY: str|None
    positionCoordinateYType: str|None

class ObservationUnit(BaseModel):
    additionalInfo: dict|None
    crossDbId: str|None
    crossName: str|None
    externalReferences: list[ExternalReference]|None
    germplasmDbId: str|None
    germplasmName: str|None
    locationDbId: str|None
    locationName: str|None
    observationUnitDbId: str|None
    observationUnitName: str|None
    observationUnitPUI: str|None
    observationUnitPosition: ObservationUnitPosition|None
    observations: list[Observation]|None
    programDbId: str|None
    programName: str|None
    seedLotDbId: str|None
    seedLotName: str|None
    studyDbId: str|None
    studyName: str|None
    treatments: list[Treatment]|None
    trialDbId: str|None
    trialName: str|None

class OntologyAnnotation(BaseModel):
    URL: str|None
    type: str|None

class Ontology(BaseModel):
    documentationLinks: list[OntologyAnnotation]|None
    ontologyDbId: str|None
    ontologyName: str|None
    version: str|None

class Method(BaseModel):
    additionalInfo: dict|None
    bibliographicalReference: str|None
    description: str|None
    externalReferences: list[ExternalReference]|None
    formula: str|None
    methodClass: str|None
    methodDbId: str|None
    methodName: str|None
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
    additionalInfo: Optional[dict]
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
    contentTypes: list[str]
    methods: list[str]
    service: str
    versions: list[str]

class ServerInfo(BaseModel):
    calls: list[Call]
    contactEmail: str|None
    documentationURL: str|None
    location: str|None
    organizationName: str|None
    organizationURL: str|None
    serverDescription: str|None
    serverName: str|None