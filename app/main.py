from fastapi import FastAPI
from app.routes import trading


app = FastAPI()


app.include_router(trading.router, prefix="/trading", tags=["trading"])