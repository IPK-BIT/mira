from fastapi import APIRouter, HTTPException, Request, status
import dataload
from icecream import ic

router = APIRouter(
    
)

@router.post("/register", tags=["Authorization"])
def get_apikey(request: Request):
    """
    ONLY ON LOCALHOST
    """
    if request.base_url.hostname in ["localhost", "127.0.0.1"]:
        return {"message": "token"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)