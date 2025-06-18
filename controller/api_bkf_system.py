from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from utility.database.database import get_db
from utility.models.model_data import SystemList
import logging

router = APIRouter(prefix="/syetem", tags=["BKF System"])

logging.basicConfig(level=logging.INFO)  # ตั้งค่า log level

@router.get("/get-bkf-system-all/")
async def get_bkf_system_all(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SystemList).order_by(asc(SystemList.seq)))
        system = result.scalars().all()

        logging.info(f"Retrieved {len(system)} records from the database")  # เพิ่มการ log ที่นี่
        return system

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")  # Log ข้อผิดพลาด
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")