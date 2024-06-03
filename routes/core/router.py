from litestar import Router
from routes.core.controllers.trial import TrialController
from routes.core.controllers.study import StudyController

CoreRouter = Router(
    path="/brapi/v2", 
    tags=["Core"],
    route_handlers=[TrialController, StudyController])