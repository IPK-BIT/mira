# MIRA

[![Documentation Status](https://readthedocs.org/projects/mira-server/badge/?version=latest)](https://mira-server.readthedocs.io/en/latest/?badge=latest)
[![Demonstrator](https://img.shields.io/badge/Demonstrator-Bridge%20core1000-blue)](https://mira.ipk-gatersleben.de)
![License](https://img.shields.io/github/license/IPK-BIT/mira)

MIRA is a FastAPI application that enables access to MIAPPE-compliant ISA Tab archives by providing BrAPI endpoints.

## Installation

In addition to the contents of this repository, there need to be two inputs available. 
- MIRA enables the access to a MIAPPE-compliant ISA Tab archive, so you need to specify in the docker-compose.yml, where the folder can be found. In the current version only one study with one assay is supported. In addition to the ISA files, a trait definition file and a data file need to be provided.
- The second input is a configuration file. This allows basic configuration and is used as a resource for the endpoint GET /serverinfo. The structure of config.yml is shown in the example below.

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

Use docker compose to install the application.

```bash
docker compose up
```

## Usage

There is a redirection on from root to /docs where you can find a documentation of the available endpoints.

In the current version the following endpoints are implemented:
- GET /observations
- GET /variables
- GET /observationunits

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)