from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from utility.database.database import get_db
from utility.models.model_data import SystemList

router = APIRouter(prefix="/syetem", tags=["BKF System"])

@router.get("/get-bkf-system-all/")
async def get_bkf_system_all(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SystemList).order_by(asc(SystemList.seq)))
        system = result.scalars().all()

        return system

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")