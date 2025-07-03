from math import ceil
from litestar import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from db.schemas import response
from db.models.models import Germplasm as DbGermplasm
from db.schemas.germplasm import Germplasm

class GermplasmController(Controller):
    path="/germplasm"

    @get('/')
    async def get_all_germplasm(self, transaction: AsyncSession, page: int|None = None, pageSize: int|None = None, germplasmDbId: str|None = None, germplasmName: str|None = None ) -> response.Response[Germplasm]: 
        if not page:
            page = 0
        if not pageSize:
            pageSize = 1000
        
        query = select(DbGermplasm)
        if germplasmDbId:
            query = query.where(DbGermplasm.germplasmDbId == germplasmDbId)
        if germplasmName:
            query = query.where(DbGermplasm.germplasmName == germplasmName)
        query_results = (await transaction.execute(query)).scalars().all()
        total_count = len(query_results)
        
        query = query.offset(page * pageSize).limit(pageSize)
        query_results = (await transaction.execute(query)).scalars().all()
        results = []
        for g in query_results:
            results.append(Germplasm(
                germplasmDbId=g.germplasmDbId,
                germplasmName=g.germplasmName,
                germplasmPUI=g.germplasmPUI,
                germplasmOrigin=g.germplasmOrigin,
                genus=g.genus,
                species=g.species,
                subtaxa=g.subtaxa,
                seedSourceDescription=g.seedSourceDescription,
            ))
        
        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    currentPage=page,
                    pageSize=pageSize,
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize)
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[]
            ),
            result=response.Result(data=results)
        )
    
    @get('/{germplasmDbId: str}/')
    async def get_one_germplasm(self, transaction: AsyncSession, germplasmDbId: str) -> response.SingleResponse[Germplasm]: 
        query = select(DbGermplasm).where(DbGermplasm.germplasmDbId == germplasmDbId)
        query_result = (await transaction.execute(query)).scalars().first()
        try:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=1000,
                        totalCount=1,
                        totalPages=1
                    ),
                    status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                    datafiles=[]
                ),
                result=Germplasm(
                    germplasmDbId=query_result.germplasmDbId
                )   
            )
        except:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=1000,
                        totalCount=0,
                        totalPages=0
                    ),
                    status=[response.Message(message="Germplasm not found", messageType=response.MESSAGETYPE.ERROR)],
                    datafiles=[]
                ),
                result=None
            )