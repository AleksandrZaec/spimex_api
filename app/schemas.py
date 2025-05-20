from pydantic import BaseModel
from datetime import datetime, date


class TradingResult(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int | None = None
    total: float | None = None
    count: int | None = None
    date: date
    created_on: datetime
    updated_on: datetime

    model_config = {
        "from_attributes": True
    }





