from litestar import Router
from routes.core.controllers.trial import TrialController
from routes.core.controllers.study import StudyController

CoreRouter = Router(
    path="/brapi/v2", 
    tags=["Core"],
    route_handlers=[TrialController, StudyController])

core_calls = [
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
        "service": "trials/{trialDbId}",
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
    }
]