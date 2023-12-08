from pydantic import BaseModel
#from pydantic.generics import GenericModel
from typing import TypeVar, Generic
from resources import schemas

T = TypeVar('T')#, bound=BaseModel)

class ServerInfoResponse(BaseModel):
    metadata: schemas.Metadata
    result: schemas.ServerInfo

class Result(BaseModel, Generic[T]):
    data: list[T]

class Response(BaseModel, Generic[T]):
    metadata: schemas.Metadata
    result: Result[T]|schemas.Table

class SingleResponse(BaseModel, Generic[T]):
    metadata: schemas.Metadata
    result: T