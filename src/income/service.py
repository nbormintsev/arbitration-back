from datetime import datetime

from src.income.crud import (
    add_new_income,
    get_income_by_client_id,
)
from src.income.schemas import IncomeResponse


async def add_client_income(
    client_id: int,
    loop_id: int,
    input_value: float,
    output_value: float,
) -> int:
    return await add_new_income(
        client_id=client_id,
        loop_id=loop_id,
        input_value=input_value,
        output_value=output_value,
        creation_time=datetime.utcnow(),
    )


async def get_client_income(client_id: int) -> list[IncomeResponse]:
    income_in_db: list | None = await get_income_by_client_id(client_id)

    return [IncomeResponse(**income) for income in income_in_db]
