from fastapi import APIRouter, status

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get("/germplasm", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_germplasm():
    return {
        "message": "not implemented"
    }
