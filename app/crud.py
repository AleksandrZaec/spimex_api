from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.models import SpimexTradingResults


async def get_last_trading_dates(session: AsyncSession, limit: int) -> List[date]:
    result = await session.execute(
        select(SpimexTradingResults.date)
        .distinct()
        .order_by(desc(SpimexTradingResults.date))
        .limit(limit)
    )
    return result.scalars().all()


async def get_dynamics(
        session: AsyncSession,
        start_date: date,
        end_date: date,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
):
    query = select(SpimexTradingResults).where(
        SpimexTradingResults.date.between(start_date, end_date)
    )
    if oil_id:
        query = query.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexTradingResults.delivery_basis_id == delivery_basis_id)

    query = query.order_by(SpimexTradingResults.date)
    result = await session.execute(query)
    return result.scalars().all()


async def get_trading_results(
        session: AsyncSession,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        limit: int = 100
):
    query = select(SpimexTradingResults).order_by(desc(SpimexTradingResults.date))
    if oil_id:
        query = query.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
    query = query.limit(limit)
    result = await session.execute(query)
    return result.scalars().all()
