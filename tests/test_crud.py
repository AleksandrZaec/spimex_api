# import pytest
# from app.crud import get_last_trading_dates, get_dynamics, get_trading_results
# from app.models import SpimexTradingResults
# from datetime import date
#
#
# @pytest.mark.asyncio
# @pytest.mark.usefixtures("test_session")
# class TestCRUD:
#
#     async def test_get_last_trading_dates(self, test_session):
#         limit = 5
#         dates = await get_last_trading_dates(test_session, limit)
#
#         assert isinstance(dates, list)
#         assert len(dates) <= limit
#         assert all(isinstance(d, date) for d in dates)
#         assert dates == sorted(dates, reverse=True)
#         assert len(dates) == len(set(dates))
#
#     async def test_get_dynamics_basic(self, test_session, date_range):
#         start, end = date_range
#         results = await get_dynamics(test_session, start, end)
#
#         assert isinstance(results, list)
#         if results:
#             assert isinstance(results[0], SpimexTradingResults)
#             for res in results:
#                 assert start <= res.date <= end
#
#     async def test_get_trading_results_no_filters(self, test_session):
#         results = await get_trading_results(test_session)
#
#         assert isinstance(results, list)
#         if results:
#             assert isinstance(results[0], SpimexTradingResults)
#         assert len(results) <= 100
#
#     async def test_get_trading_results_with_filters(self, test_session, filters):
#         results = await get_trading_results(
#             test_session,
#             filters["oil_id"],
#             filters["delivery_type_id"],
#             filters["delivery_basis_id"],
#             limit=50
#         )
#
#         assert isinstance(results, list)
#         assert len(results) <= 50
#         for res in results:
#             assert res.oil_id == filters["oil_id"]
#             assert res.delivery_type_id == filters["delivery_type_id"]
#             assert res.delivery_basis_id == filters["delivery_basis_id"]


