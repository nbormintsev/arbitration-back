from pydantic import BaseModel


class LoopsUpdateResponse(BaseModel):
    message: str
