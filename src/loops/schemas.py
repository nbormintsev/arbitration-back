from pydantic import BaseModel


class LoopsUpdateResponse(BaseModel):
    message: str


class PlatformsResponse(BaseModel):
    name: str


class CurrenciesResponse(BaseModel):
    name: str
