from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from icecream import ic

from brapi import phenotyping, germplasm, core, genotyping
import dataload

app = FastAPI(
    title="Bridge MIRA",
    description="MIRA is a FastAPI application that enables access to MIAPPE-compliant ISA Tab archives by providing BrAPI endpoints. This server loads the core1000 BRIDGE phenotyping dataset provided by https://bridge.ipk-gatersleben.de"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def init_miappe():
    dataload.read_miappe('/data')

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

@app.get('/favicon.ico', include_in_schema=False)
def favicon():
    return FileResponse('favicon.ico')

app.include_router(core.router, tags=["BrAPI Core"])
app.include_router(phenotyping.router, tags=["BrAPI Phenotyping"])
app.include_router(genotyping.router, tags=["BrAPI Genotyping"])
app.include_router(germplasm.router, tags=["BrAPI Germplasm"])

try:
    if dataload.config['server']['requireAuthorization']:
        from authorization import authorization
        app.include_router(authorization.router, tags=["Authorization"])
except:
    None