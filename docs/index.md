# MIRA - Enabling Access to MIAPPE compliant ISArchives through BrAPI

## Use Case
Phenotyping datasets are often available as [MIAPPE](https://www.miappe.org/) compliant [ISA Tab](https://isa-specs.readthedocs.io/en/latest/isatab.html) in repositories. However, the programmatic use of those datasets is limited. To enable access to such data products, MIRA is transforming them and provides [BrAPI](https://brapi.org/) endpoints accordingly. This allows developers to use the data products in their applications. In a demonstrator [DivBrowse](https://divbrowse.ipk-gatersleben.de) utilizes the [BRIDGE core1000 dataset](https://bridge.ipk-gatersleben.de/) to color results of a dimensionality reduction of genotypic data by phenotypic observations results.

## Installation

First, clone the repository to your local machine.

```
git clone https://github.com/IPK-BIT/mira.git
```

After that, several additional resources have to be provided, in order for MIRA to run. 

### MIAPPE ISArchive

MIRA uses MIAPPE compliant ISA Tab archives as primary input. Those MIAPPE ISArchives are made available by placing the ``data/`` directory next to the ``docker-compose.yml``. A [mapping](miappe.md) of MIAPPE to ISA Tab and BrAPI is provided with this documentation. For the current version of MIRA, only ISArchives with one study and one assay are valid input.

### Configuration File

A configuration file ``config.yml`` is needed to configure server information and activate or deactivate modules not required. The configuration file needs also to be placed next to the ``docker-compose.yml``. An example configuration file is provided:

```
server:
  name: 'MIRA Testserver'
  description: 'Some description for your new MIRA server'
  documentation: 'http://<your info>/docs'
  requireAuthorization: false
contact:
  organization:
    name: 'Your Organization'
    url: 'https://organization.org'
    location: 'Country'
  mail: 'mail@example.com'
module:
  enableCore: true
  enablePhenotyping: true
  enableGenotyping: false
  enableGermplasm: false
```

### Running with HTTPS 

For running with HTTPS, the certificate and private key need to be copied into the ``/app`` directory. 
For testing locally, it's possible to use [mkcert](https://github.com/FiloSottile/mkcert) to generate valid certificate and private key files. 

### Starting the MIRA Server

Use docker compose to install the application.

```bash
docker compose up
```

## Usage

All available endpoints of a specific MIRA Server are automatically documented and made available through ```/docs```. The root path is also redirected to the documentation.
For a more detailed description of possible endpoints, use the official [BrAPI specifications](https://brapi.org/specification) or the [API documentation](brapi.md) provided here.