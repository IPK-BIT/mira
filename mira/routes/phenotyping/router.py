from litestar import Router

from routes.phenotyping.controllers.observation import ObservationController
from routes.phenotyping.controllers.observationunit import ObservationUnitController
from routes.phenotyping.controllers.observationvariable import ObservationVariableController

PhenotypingRouter = Router(
    path="/brapi/v2",
    tags=["Phenotyping"],
    route_handlers=[ObservationController, ObservationUnitController, ObservationVariableController],
)

phenotyping_calls = [
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
        "service": "variables/{observationVariableDbId}",
        "versions": [
            "2.1"
        ]
    },
]