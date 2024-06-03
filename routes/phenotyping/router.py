from litestar import Router

from routes.phenotyping.controllers.observation import ObservationController
from routes.phenotyping.controllers.observationunit import ObservationUnitController
from routes.phenotyping.controllers.observationvariable import ObservationVariableController

PhenotypingRouter = Router(
    path="/brapi/v2",
    tags=["Phenotyping"],
    route_handlers=[ObservationController, ObservationUnitController, ObservationVariableController],
)
