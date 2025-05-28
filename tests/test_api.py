import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestLastTradingDatesAPI:
    async def test_valid_limit(self, ac: AsyncClient, test_cache):
        response = await ac.get("/trading/last_trading_dates?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    @pytest.mark.parametrize(
        "query, loc, err_type, msg_part",
        [
            ("", ["query", "limit"], "missing", None),
            ("?limit=0", ["query", "limit"], "greater_than", "greater than 0"),
            ("?limit=-3", ["query", "limit"], "greater_than", "greater than 0"),
            ("?limit=abc", ["query", "limit"], "int_parsing", "valid integer"),
        ],
    )
    async def test_invalid_limits(self, ac: AsyncClient, test_cache, query, loc, err_type, msg_part):
        response = await ac.get(f"/trading/last_trading_dates{query}")
        assert response.status_code == 422
        errors = response.json().get("detail", [])
        assert any(
            e["loc"] == loc and e["type"] == err_type and (msg_part is None or msg_part in e["msg"])
            for e in errors
        ), f"Unexpected validation errors: {errors}"


@pytest.mark.asyncio
class TestDynamicsAPI:
    valid_start_date = "2024-01-01"
    valid_end_date = "2024-01-10"

    def assert_result_item_structure(self, item, example_item):
        for key, example_value in example_item.items():
            assert key in item, f"Missing key '{key}' in item"
            if isinstance(example_value, float):
                assert isinstance(item[key], (float, int)), f"Key '{key}' has wrong type"
            else:
                assert isinstance(item[key], type(example_value)), f"Key '{key}' has wrong type"

    async def test_dynamics_start_date_after_end_date(self, ac: AsyncClient, test_cache):
        response = await ac.get("/trading/dynamics", params={
            "start_date": self.valid_end_date,
            "end_date": self.valid_start_date,
        })
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "start_date must be before or equal to end_date"

    @pytest.mark.parametrize(
        "params, error_loc",
        [
            ({}, ["query", "start_date"]),
            ({"end_date": "2024-01-10"}, ["query", "start_date"]),
            ({"start_date": "2024-01-01"}, ["query", "end_date"]),
            ({"start_date": "not-a-date", "end_date": "2024-01-10"}, ["query", "start_date"]),
            ({"start_date": "2024-01-01", "end_date": "not-a-date"}, ["query", "end_date"]),
        ],
    )
    async def test_dynamics_validation_errors(self, ac: AsyncClient, params, error_loc):
        response = await ac.get("/trading/dynamics", params=params)
        assert response.status_code == 422
        errors = response.json().get("detail", [])
        assert any(e["loc"] == error_loc for e in errors)


@pytest.mark.asyncio
class TestTradingResultsAPI:
    async def test_trading_results_success(self, ac: AsyncClient, test_cache):
        response = await ac.get("/trading/trading_results")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_trading_results_with_valid_params(self, ac: AsyncClient, test_cache):
        params = {
            "oil_id": "A100",
            "delivery_type_id": "DT001",
            "delivery_basis_id": "DB001",
        }
        response = await ac.get("/trading/trading_results", params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_trading_results_invalid_params(self, ac: AsyncClient):
        response = await ac.get("/trading/trading_results", params={"oil_id": {"invalid": "value"}})
        assert response.status_code == 422

        response = await ac.get("/trading/trading_results", params={"unknown_param": "value"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

