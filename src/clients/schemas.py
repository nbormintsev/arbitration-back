from datetime import timedelta, datetime

from pydantic import BaseModel


class SettingsCreationResponse(BaseModel):
    id: int


class SettingsCreation(BaseModel):
    client_id: int
    notification_min_spread: float
    language: str
    timezone_offset: timedelta


class SettingsInfoResponse(BaseModel):
    notification_min_spread: float
    language: str
    timezone_offset: timedelta


class SettingsUpdate(BaseModel):
    notification_min_spread: float
    language: str
    timezone_offset: timedelta


class DeviceCreationResponse(BaseModel):
    id: int


class DeviceCreation(BaseModel):
    client_id: int
    device_hash: bytes
    device_name: str


class DeviceInfo(BaseModel):
    id: int
    device_name: str
    last_login_date: datetime
