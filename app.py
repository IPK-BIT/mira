import os
import yaml

from rich import get_console

from litestar import Litestar, get
from litestar.openapi import OpenAPIConfig
from litestar.config.cors import CORSConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from litestar.types import ASGIApp, Scope, Receive, Send

from etl.isatab import ingest_isatab
from etl.arc import ingest_arc

from routes.core.router import CoreRouter
from routes.germplasm.router import GermplasmRouter
from routes.phenotyping.router import PhenotypingRouter

from db.models.db_connect import db_connection, provide_transaction
import base64

def load_config():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config

async def init():
    app.state.console = get_console()
    app.state.config = load_config()
    if app.state.config['format'] == 'isa-tab':
        data = ingest_isatab.extract(app.state.config['data'])
        ingest_isatab.transform_and_load(data, app.state.config['data'])
    elif app.state.config['format'] == 'arc':
        data = ingest_arc.extract(app.state.config['data'])
        ingest_arc.transform_and_load(data, app.state.config['data'])
    else:
        raise ValueError("Invalid format in config")
    return

async def exit():
    os.remove('miappe.db')

cors_config = CORSConfig(
    allow_origins=['*'],
    allow_methods=['GET']
)


@get('/brapi/v2/serverinfo', include_in_schema=False)
async def server_info() -> dict:
    return {
        "metadata": {
            "datafiles": [],
            "pagination": {
            "currentPage": 0,
            "pageSize": 1000,
            "totalCount": 10,
            "totalPages": 1
            },
            "status": [
            {
                "message": "Request accepted, response successful",
                "messageType": "INFO"
            }
            ]
        },
        "result": {
            "calls": [
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "trials",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "trial/{trialDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "studies",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "studies/{studyDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "germplasm",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "germplasm/{germplasmDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observationunits",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observationunits/{observationUnitDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observations",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observations/{observationDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "variables/{observationVariableDbId}",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "variables",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observations/table",
                "versions": [
                    "2.1"
                ]
            }
            ],
            "contactEmail": "contact@institute.org",
            "documentationURL": "institute.org/server",
            "location": "USA",
            "organizationName": "The Institute",
            "organizationURL": "institute.org/home",
            "serverDescription": "The BrAPI Test Server\nWeb Server - Apache Tomcat 7.0.32\nDatabase - Postgres 10\nSupported BrAPI Version - V2.0",
            "serverName": "The BrAPI Test Server"
        }
        }

scalar_plugin = ScalarRenderPlugin(version="1.19.5", path="/scalar")


middlewares = []
config = load_config()
if config.get('aai', False):
    basic_auth = config['aai'][0]['username'] + ':' + config['aai'][0]['password']
    token = base64.b64encode(basic_auth.encode('utf-8'))
    def basic_auth_factory(app:ASGIApp)->ASGIApp:
        async def basic_auth(scope:Scope, receive:Receive, send:Send):
            if scope['type'] == 'http':
                headers = dict(scope['headers'])
                if headers.get(b'authorization', b'') != b'Basic ' + token:
                    await send({
                        'type': 'http.response.start',
                        'status': 401,
                        'headers': [
                            [b'www-authenticate', b'Basic realm="Login Required"']
                        ]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b'Unauthorized'
                    })
                    return
            await app(scope, receive, send)
        return basic_auth
    middlewares.append(basic_auth_factory)


app = Litestar(
    route_handlers=[server_info, CoreRouter, GermplasmRouter, PhenotypingRouter],
    cors_config=cors_config,
    lifespan=[db_connection],
    middleware=middlewares,
    on_startup=[init],
    on_shutdown=[exit],
    dependencies={'transaction': provide_transaction},
    openapi_config=OpenAPIConfig(
        title="MIRA",
        version="0.1.0",
        description="MIRA is a BrAPI server deployed on top of a MIAPPE compliant ISArchive.",
        render_plugins=[ScalarRenderPlugin()],
    ),
)
