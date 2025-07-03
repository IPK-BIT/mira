import os
import yaml
import json
import base64

from rich import get_console

from litestar import Litestar, get
from litestar.datastructures.state import State
from litestar.openapi import OpenAPIConfig
from litestar.config.cors import CORSConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.types import ASGIApp, Scope, Receive, Send

from db.models.db_connect import db_connection, provide_transaction
from etl.arc.ingest import ingest

from routes.core.router import CoreRouter, core_calls
from routes.germplasm.router import GermplasmRouter, germplasm_calls
from routes.phenotyping.router import PhenotypingRouter, phenotyping_calls

def load_config():
    with open('../config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config

async def init():
    app.state.console = get_console()
    app.state.config = load_config()
    if app.state.config['format']=='arc':
        ingest(app.state.config['data'])
    return

async def exit():
    os.remove('miappe.db')
    
@get('/brapi/v2/serverinfo')
async def server_info(state: State) -> dict:   
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
                    "message": "Success",
                    "messageType": "INFO"
                }
            ]
        },
        "result": {
            "calls": core_calls+germplasm_calls+phenotyping_calls,
            "contactEmail": state.config['server']['contact'],
            "documentationURL": state.config['server']['documentation'],
            "location": state.config['server']['location'],
            "organizationName": state.config['server']['organization']['name'],
            "organizationURL": state.config['server']['organization']['url'],
            "serverDescription": state.config['server']['description'],
            "serverName": state.config['server']['name']
        }
    }

cors_config = CORSConfig(
    allow_origins=['*'],
    allow_methods=['GET'],
    allow_headers=['*'],
    allow_credentials=True,
)

scalar_plugin = ScalarRenderPlugin(path="/scalar")

middlewares = []
config = load_config()
if config.get('aai', False):
    basic_auth = config['aai'][0]['username'] + ':' + config['aai'][0]['password']
    token = base64.b64encode(basic_auth.encode('utf-8'))
    def basic_auth_factory(app:ASGIApp)->ASGIApp:
        async def basic_auth(scope:Scope, receive:Receive, send:Send):
            if scope['type'] == 'http':
                if scope['method'] == 'OPTIONS':
                    await app(scope, receive, send)
                    return
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