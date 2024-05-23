from datetime import datetime

from src.database import database_manager


async def add_new_income(
    client_id: int,
    loop_id: int,
    input_value: float,
    output_value: float,
    creation_time: datetime,
) -> int:
    pool = await database_manager.get_pool()

    return await pool.fetchval(
        """
        insert into
            client_income (
                client,
                loop,
                input_value,
                output_value,
                creation_time
            )
        values
            ($1, $2, $3, $4, $5)
        returning
            id
        """,
        client_id,
        loop_id,
        input_value,
        output_value,
        creation_time
    )


async def get_income_by_client_id(client_id: int):
    pool = await database_manager.get_pool()

    return await pool.fetch(
        """
        select
            *
        from
            client_income
        where
            client = $1
        order by
            id
        """,
        client_id
    )
