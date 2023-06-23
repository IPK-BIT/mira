from fastapi import APIRouter, status

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get("/samples", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_samples():
    return {
        "message": "not implemented"
    }