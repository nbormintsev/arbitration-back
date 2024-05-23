from typing import Any

from fastapi import APIRouter, Depends

from src.auth.dependencies import validate_access_token
from src.income.schemas import IncomeResponse
from src.income.service import add_client_income, get_client_income

router = APIRouter()


@router.post(path="/add")
async def add_authenticated_client_income(
    loop_id: int,
    input_value: float,
    output_value: float,
    token_payload: dict[str, Any] = Depends(validate_access_token),
) -> int:
    return await add_client_income(
        client_id=token_payload.get("sub"),
        loop_id=loop_id,
        input_value=input_value,
        output_value=output_value,
    )


@router.get(path="/graph")
async def get_authenticated_client_income(
    token_payload: dict[str, Any] = Depends(validate_access_token)
) -> list[IncomeResponse]:
    return await get_client_income(token_payload.get("sub"))
