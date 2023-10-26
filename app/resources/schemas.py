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
    referenceId: str|None = None
    referenceSource: str|None = None

class Geometry(BaseModel):
    coordinates: list[float]|None = None
    type: str

class GeoCoordinates(BaseModel):
    geometry: Geometry
    type: str

class Season(BaseModel):
    seasonDbId: str|None = None
    seasonName: str|None = None
    year: str|None = None

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
    methodPUI: str|None = None
    ontologyReference: Ontology|None = None

class ValueAnnotation(BaseModel):
    label: str|None = None
    value: str|None = None

class ValueRange(BaseModel):
    categories: list[ValueAnnotation]|None = None
    maximumValue: str|None = None
    minimumValue: str|None = None

class Trait(BaseModel):
    additionalInfo: dict|None = None
    alternativeAbbreviations: list[str]|None = None
    attribute: str|None = None
    attributePUI: str|None = None
    entity: str|None = None
    entityPUI: str|None = None
    externalReferences: list[ExternalReference]|None = None
    mainAbbreviation: str|None = None
    ontologyReference: Ontology|None = None
    status: str|None = None
    synonyms: list[str]|None = None
    traitClass: str|None = None
    traitDbId: str|None = None
    traitDescription: str|None = None
    traitName: str|None = None
    traitPUI: str|None = None

class Scale(BaseModel):
    additionalInfo: dict|None = None
    dataType: str|None = None
    decimalPlaces: int|None = None
    externalReferences: list[ExternalReference]|None = None
    ontologyReference: Ontology|None = None
    scaleDbId: str|None = None
    scaleName: str|None = None
    scalePUI: str|None = None
    units: str|None = None
    validValues: ValueRange|None = None

class ObservationVariable(BaseModel):
    additionalInfo: dict|None = None
    commonCropName: str|None = None
    contextOfUse: list[str]|None = None
    defaultValue: str|None = None
    documentationURL: str|None = None
    externalReferences: list[ExternalReference]|None = None
    growthStage: str|None = None
    institution: str|None = None
    language: str|None = None
    method: Method|None = None
    observationVariableDbId: str|None = None
    observationVariableName: str|None = None
    observationVariablePUI: str|None = None
    ontologyReference: Ontology|None = None
    scale: Scale|None = None
    scientist: str|None = None
    status: str|None = None
    submissionTimestamp: str|None = None
    synonyms: list[str]|None = None
    trait: Trait|None = None

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

class Donor(BaseModel):
    donorAccessionNumber: str|None = None
    donorInstituteCode: str|None = None

class Origin(BaseModel):
    coordinateUncertainty: str|None = None
    coordinates: GeoCoordinates|None = None

class Synonym(BaseModel):
    synonym: str|None = None
    type: str|None = None

class TaxonRef(BaseModel):
    sourceName: str|None = None
    taxonId: str|None = None

class StorageType(BaseModel):
    code: str|None=None
    description: str|None=None

class Germplasm(BaseModel):
    accessionNumber: str|None = None
    acquisitionDate: str|None = None
    additionalInfo: dict|None = None
    biologicalStatusOfAccessionCode: str|None = None
    biologicalStatusOfAccessionDescription: str|None = None
    breedingMethodDbId: str|None = None
    breedingMethodName: str|None = None
    collection: str|None = None
    commonCropName: str|None = None
    countryOfOriginCode: str|None = None
    defaultDisplayName: str|None = None
    documentationURL: str|None = None
    donors: list[Donor]|None = None
    externalReferences: list[ExternalReference]|None = None
    genus: str|None = None
    germplasmDbId: str|None = None
    germplasmName: str|None = None
    germplasmOrigin: list[Origin]|None = None
    germplasmPUI: str|None = None
    germplasmPreprocessing: str|None = None
    instituteCode: str|None = None
    instituteName: str|None = None
    pedigree: str|None = None
    seedSource: str|None = None
    seedSourceDescription: str|None = None
    species: str|None = None
    speciesAuthority: str|None = None
    storageTypes: list[StorageType]|None = None,
    subtaxa: str|None = None
    subtaxaAuthority: str|None = None
    synonyms: list[Synonym]|None = None
    taxonIds: list[TaxonRef]|None = None

class Contact(BaseModel):
    contactDbId: str|None = None
    email: str|None = None
    instituteName: str|None = None
    name: str|None = None
    orcid: str|None = None
    type: str|None = None

class Dataset(BaseModel):
    datasetPUI: str|None = None
    license: str|None = None
    publicReleaseDate: str|None = None
    submissionDate: str|None = None

class Publication(BaseModel):
    publicationPUI: str|None = None
    publicationReference: str|None = None

class Trial(BaseModel):
    active: bool|None = None
    additionalInfo: dict|None = None
    commonCropName: str|None = None
    contacts: list[Contact]|None = None
    datasetAuthorships: list[Dataset]|None = None
    documentationURL: str|None = None
    endDate: str|None = None
    externalReferences: list[ExternalReference]|None = None
    programDbId: str|None = None
    programName: str|None = None
    publications: list[Publication]|None = None
    startDate: str|None = None
    trialDbId: str|None = None
    trialDescription: str|None = None
    trialName: str|None = None
    trialPUI: str|None = None

class DataLink(BaseModel):
    dataFormat: str|None = None
    description: str|None = None
    fileFormat: str|None = None
    name: str|None = None
    provenance: str|None = None
    scientificType: str|None = None
    url: str|None = None
    version: str|None = None

class EnvironmentalParameter(BaseModel):
    description: str|None = None
    parameterName: str|None = None
    parameterPUI: str|None = None
    unit: str|None = None
    unitPUI: str|None = None
    value: str|None = None
    valuePUI: str|None = None

class ExperimentalDesign(BaseModel):
    description: str|None = None
    PUI: str|None = None

class GrowthFacility(BaseModel):
    description: str|None = None
    PUI: str|None = None

class Timestamp(BaseModel):
    timestamp: str|None = None
    version: str|None = None

class Study(BaseModel):
    active: bool|None = None
    additionalInfo: dict|None = None
    commonCropName: str|None = None
    contacts: list[Contact]|None = None
    culturalPractices: str|None = None
    dataLinks: list[DataLink]|None = None
    documentationURL: str|None = None
    endDate: str|None = None
    environmentParameters: list[EnvironmentalParameter]|None = None
    experimentalDesign: ExperimentalDesign|None = None
    externalReferences: list[ExternalReference]|None = None
    growthFacility: GrowthFacility|None = None
    lastUpdate: Timestamp|None = None
    license: str|None = None
    locationDbId: str|None = None
    locationName: str|None = None
    observationLevels: list[ObservationLevel]|None = None
    observationUnitsDescription: str|None = None
    observationVariableDbIds: list[str]|None = None
    seasons: list[str]|None = None
    startDate: str|None = None
    studyCode: str|None = None
    studyDbId: str|None = None
    studyDescription: str|None = None
    studyName: str|None = None
    studyPUI: str|None = None
    studyType: str|None = None
    trialDbId: str|None = None
    trialName: str|None = None

class Institute(BaseModel):
    institueCode: str|None = None
    instituteName: str|None = None

class CollectingInstitute(Institute):
    instituteAddress: str|None = None

#Why is the location given as decimal and degrees? And why is it a string not an int?
class CollectingSite(BaseModel):
    coordinateUncertainty: str|None = None
    elevation: str|None = None
    #FIXME: correct example? WGS84 is spatialReferenceSystem, GPS is in text example for georeferencing method
    georeferencingMethod: str|None = None
    latitudeDecimal: str|None = None
    latitudeDegrees: str|None = None
    locationDescription: str|None = None
    longitudeDecimal: str|None = None
    longitudeDegrees: str|None = None
    spatialReferenceSystem: str|None = None

class CollectingInfo(BaseModel):
    collectingDate: str|None = None
    #FIXME: Why does it have an address but not breedingInstitute?
    collectingInstitutes: list[CollectingInstitute]|None = None
    collectingMissionIdentifier: str|None = None
    collectingNumber: str|None = None
    collectingSite: CollectingSite|None = None

class DonorInfo(Donor):
    donorInstitute: Institute|None = None

#TODO: introduce Enums
class GermplasmMCPD(BaseModel):
    accessionNames: list[str]|None = None
    accessionNumber: str|None = None
    acquisitionDate: str|None = None
    acquisitionSourceCode: str|None = None
    #FIXME: should be alternateIds to comply with BrAPI naming scheme
    alternateIDs: list[str]|None = None
    ancestralData: str|None = None
    biologicalStatusOfAccessionCode: str|None = None
    breedingInstitutes: list[Institute]|None = None
    collectingInfo: CollectingInfo
    commonCropName: str|None = None
    countryOfOrigin: str|None = None
    donorInfo: DonorInfo|None = None
    genus: str|None
    germplasmDbId: str|None = None
    germplasmPUI: str|None = None
    instituteCode: str|None = None
    mlsStatus: str|None = None
    remarks: str|None = None
    safetyDuplicateInstitutes: list[Institute]|None = None
    species: str|None = None
    speciesAuthority: str|None = None
    storageTypeCodes: list[str]|None = None
    subtaxon: str|None = None
    subtaxonAuthority: str|None = None

class ObservationVariableReference(BaseModel):
    observationVariableDbId: str|None = None
    observationVariableName: str|None = None

#TODO: add enum for header
class Table(BaseModel):
    data: list[list[str]]
    headerRow: list[str]
    observationVariables: list[ObservationVariableReference]