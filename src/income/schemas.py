from datetime import datetime

from pydantic import BaseModel


class IncomeResponse(BaseModel):
    id: int
    client: int
    loop: int
    input_value: float
    output_value: float
    creation_time: datetime
