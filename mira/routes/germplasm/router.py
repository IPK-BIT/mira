from litestar import Router

from routes.germplasm.controllers.germplasm import GermplasmController

GermplasmRouter = Router(
    path="/brapi/v2",
    tags=["Germplasm"],
    route_handlers=[GermplasmController],
)

germplasm_calls = [
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
    }
]