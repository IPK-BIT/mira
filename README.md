# MIRA

## Overview

MIRA is a software solution designed to deploy a BrAPI server on top of a FAIR Digital Object (FDO) that fulfills the MIAPPE requirements. It provides flexibility to run the server either as a Docker container or directly from the source code.

## Features

- Deploys a BrAPI server compliant with MIAPPE standards.
- Supports deployment via Docker or source code.
- Supports ARC RO-Crate format for input

## Installation

### Using Docker

1. Ensure Docker is installed on your system.
2. Pull the Docker image:
    ```bash
    docker pull mira:latest
    ```
3. Run the container:
    ```bash
    docker run -p 8000:8000 mira:latest
    ```

### From Source

1. Clone the repository:
    ```bash
    git clone https://github.com/IPK-BIT/mira.git
    cd mira
    ```
2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. Add ./config.yml:
    ```yml
    format: <input-format>
    data: '<path-to-data>'
    aai:
    - method: basic
        username: <username>
        password: <password>
    server:
        contact: <contact-email>
        documentation: <documentation-url>
        location: <country-name>
        organization: 
            name: <organization-name>
            url: <organization-website>
        description: |
            <server-description>
        name: <server-name>
    ```
3. Start the server:
    ```bash
    cd mira
    litestar run
    ```

## Development

### Prerequisites

- Python 3.12 or higher
- Poetry

### Setting Up the Development Environment

1. Clone the repository:
    ```bash
    git clone https://github.com/IPK-BIT/mira.git
    cd mira
    ```
2. Install dependencies:
    ```bash
    poetry install
    ```
3. Add ./config.yml:
    ```yml
    format: <input-format>
    data: '<path-to-data>'
    aai:
    - method: basic
        username: <username>
        password: <password>
    server:
        contact: <contact-email>
        documentation: <documentation-url>
        location: <country-name>
        organization: 
            name: <organization-name>
            url: <organization-website>
        description: |
            <server-description>
        name: <server-name>
    ```
4. Run development server:
    ```bash
    cd mira
    poetry run litestar run --debug --reload
    ```

## Usage

Once the server is running, you can access the BrAPI endpoint documentation at `http://localhost:8000/schema`.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
