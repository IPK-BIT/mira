from fastapi import Depends
from typing import Annotated

async def common_parameters(page: int|None = None, pageSize: int|None = None):
    return {"page": page, "pageSize": pageSize}

CommonsDep = Annotated[dict, Depends(common_parameters)]