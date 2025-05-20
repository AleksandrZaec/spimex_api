from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date
from app.database import get_session
from app.crud import get_last_trading_dates, get_dynamics, get_trading_results
from app.schemas import TradingResult

router = APIRouter()


@router.get("/last_trading_dates")
async def last_trading_dates(
        limit: int = Query(..., gt=0),
        session: AsyncSession = Depends(get_session)
):
    return await get_last_trading_dates(session, limit)


@router.get("/dynamics", response_model=list[TradingResult])
async def dynamics(
        start_date: date = Query(...),
        end_date: date = Query(...),
        oil_id: Optional[str] = Query(None),
        delivery_type_id: Optional[str] = Query(None),
        delivery_basis_id: Optional[str] = Query(None),
        session: AsyncSession = Depends(get_session)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before or equal to end_date")
    return await get_dynamics(session, start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)


@router.get("/trading_results", response_model=list[TradingResult])
async def trading_results(
        oil_id: Optional[str] = Query(None),
        delivery_type_id: Optional[str] = Query(None),
        delivery_basis_id: Optional[str] = Query(None),
        session: AsyncSession = Depends(get_session)
):
    return await get_trading_results(session, oil_id, delivery_type_id, delivery_basis_id)
