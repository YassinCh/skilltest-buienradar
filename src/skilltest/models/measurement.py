from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


# TODO: Fix string usage to actually use a proper reference to the WheatherStation ID
class Measurement(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("stationid", "timestamp", sqlite_on_conflict="IGNORE"),
    )
    measurementid: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(index=True)
    temperature: Optional[float] = None
    groundtemperature: Optional[float] = None
    feeltemperature: Optional[float] = None
    windgusts: Optional[float] = None
    windspeedbft: Optional[int] = None
    humidity: Optional[float] = None
    sunpower: Optional[float] = None
    stationid: int = Field(foreign_key="weatherstation.stationid")
