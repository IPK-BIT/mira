# ARC Prerequisites

## Knowledge Representation within the ARC

MIRA uses an ETL pipeline in the setup phase of the BrAPI server to load the content of the ARC. First the RO-Crate and then the relevant resources are read and loaded into an internal database. This database stores the research data in the BrAPI data model and provides the interface for data access by the BrAPI endpoints.

### RO-Crate Ingestion

The ARC RO-Crate builds a graph describing the ARC Scaffold. Its nodes are the entities in the ARC data model which describe the experiments documented in the ARC. To extract the information the ETL Pipeline starts at the root node `./` and loads the investigation information. From there it traverses the rest of the graph following the relationships from each entity to the next.

**Trial**

The BrAPI Trial entity maps to the ISA Investigation. From the investigation, which is also the root element in the RO-Crate graph, the `identifier`, `name` and `license` are extracted. From the root element the graph is further traversed to the study entities.

**Study**

The ISA Study maps to the BrAPI Study entity. From the study, the `identifier` and `name` as well as the `identifier` and `name` of the investigation are extracted. The study needs to define a `Growth` protocol, which needs to be applied in the study's processes. Following the processes, the graph is further traversed to extract the source materials and samples.

**Germplasm**

The ISA Source Material maps to the BrAPI Germplasm entitiy. From the source material the following ontology annotated terms are extracted from the `additionalProperties` of the object of the process:

- `Genus (MIAPPE:0041)`
- `Species (MIAPPE:0042)`
- `Infraspecific name (MIAPPE:0043)`
- `Material source DOI (MIAPPE:0051)`
- `Material source latitude (MIAPPE:0052)`
- `Material source longitude (MIAPPE:0053)`
- `Material source coordinates uncertainty (MIAPPE:0055)`
- `Material source description (MIAPPE:0056)`

**Observation Unit**

The ISA Sample maps to the BrAPI Observation Unit entity. From the sample `name` and `identifier` are extracted from the results of the process as well as the `name` of the process's object and the `name` and `identifier` of the study and `name` and `identifier` of the investigation.

### Trait Definitions

With MIAPPE a trait definition file describes the BrAPI Observation Variables. This file needs to be located within the corresponding study directory inside the `resources` directory and needs to be named `tdf.tsv`. It is a tab-separated values file with the headers:

- `Variable ID`: Internal identifier of the observation variable
- `Variable Name`: Observation variable Name
- `Variable Accession Number`: PUI of the observation variable
- `Trait`: Trait name
- `Trait Accession Number`: PUI of the trait
- `Trait Class`: Enum of `morphological`, `agronomical`, `phenological`, `abiotic stress`, `biotic stress`, `physiological` or `quality` 
- `Method`: Method name
- `Method Accession Number`: PUI of the method
- `Method Description`: Human readable description of the method
- `Reference associated to the method`: Literature reference for the method
- `Scale`: Scale name
- `Scale Accession Number`: PUI of the scale
- `Scale Type`: Enum of `Numerical`, `Nominal` or `Ordinal`
- `Scale Values`: either scale unit or semicolon separated list of `<code>:<value>` pairs
- `Time scale`: *ignored*

An example is given below:

```tsv linenums="1" title="./studies/myStudy/resources/tdf.tsv"
Variable ID	Variable Name	Variable Accession Number	Trait	Trait Accession Number	Trait Class	Method	Method Accession Number	Method Description	Reference associated to the method	Scale	Scale Accession Number	Scale Type	Scale Values	Time scale
CONVAR	Row-Type convarity		Row-Type convarity		morphological	Row-Type Estimation				1to5RowType		Nominal	"1:'convar. distichon';2:'convar. deficiens';3:'convar. labile';4:'convar. intermedium';5:'convar. vulgare/convar. hexastichon'"	
AWNS_LENGTH	Awns length 		Awns length		morphological	Awns length Measurement				Centimeter		Numerical	cm	
```

### Observations

The actual observation data of a MIAPPE described dataset is stored in a data file, resulting of processes of executions of a `Phenotyping` protocol. This datafile is located with the assay directory in the `dataset` directory and is named `df.tsv`. It needs to be in long format with the headers:

- `Assay Name`: Sample name
- `Date`: Observation date, recommended in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- `Trait`: Variable ID of the trait definition file
- `Value`: Value of the observation

An example is given below:
```tsv linenums="1" title="./assays/myAssay/dataset/df.tsv"
Assay Name	Date	Trait	Value
HOR 4402_1105630	Tue Sep 20 00:00:00 UTC 2016	SPIKE_LENGTH	9.0
HOR 4430_1105637	Mon Sep 12 00:00:00 UTC 2016	SPIKE_LENGTH	10.0
```

## Frequently Asked Questions

### Where do I find more detailed information about MIAPPE?

The MIAPPE standard is documented within its [GitHub Repository](https://github.com/MIAPPE/MIAPPE). You can find the [mapping](https://github.com/MIAPPE/MIAPPE/blob/master/Mapping/MIAPPE_Checklist_Mapping.tsv) to ISA and BrAPI as well as general documentation. For a guide how to write ISA Tab, you can find information in the respective [GitHub Repository](https://github.com/MIAPPE/ISA-Tab-for-plant-phenotyping).

### Where do I find more information on ARC's?

You can find relevant resources for everything related to the ARC on the [website](https://arc-rdm.org). There you can find information on the [Documentation Principles](https://arc-rdm.org/details/documentation-principle/) as well as the [ARC Data Model](https://arc-rdm.org/details/arc-data-model/).

### Why is the data file required to be in long format?

Each observation stores a date when this observation was made. To avoid overcomplicated templates, the long format offers the simplest way of avoiding information loss.

[Submit new Questions](https://github.com/IPK-BIT/mira/discussions/new?category=q-a){ .md-button .md-button--primary}