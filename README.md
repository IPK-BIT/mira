# MIRA

MIRA is a FastAPI application that enables access to MIAPPE-compliant ISA Tab archives by providing BrAPI endpoints.

## Installation

Use docker compose to install the application.

```bash
docker compose up
```

## Usage

There is a redirection on from root to /docs were you can find a documentation of the available endpoints.

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