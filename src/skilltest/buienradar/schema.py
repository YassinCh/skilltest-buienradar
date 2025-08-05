from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StationMeasurement(BaseModel):
    """Weather station measurement data from Buienradar API"""

    model_config = ConfigDict(extra="ignore")

    id: int = Field(alias="$id")
    station_id: int = Field(alias="stationid")
    station_name: str = Field(alias="stationname")
    lat: float = Field(alias="lat")
    lon: float = Field(alias="lon")
    regio: str = Field(alias="regio")
    timestamp: datetime = Field(alias="timestamp")
    weather_description: str = Field(alias="weatherdescription")
    wind_direction: Optional[str] = Field(default=None, alias="winddirection")
    temperature: Optional[float] = Field(default=None, alias="temperature")
    ground_temperature: Optional[float] = Field(default=None, alias="groundtemperature")
    feel_temperature: Optional[float] = Field(default=None, alias="feeltemperature")
    wind_gusts: Optional[float] = Field(default=None, alias="windgusts")
    wind_speed: Optional[float] = Field(default=None, alias="windspeed")
    wind_speed_bft: Optional[int] = Field(default=None, alias="windspeedBft")
    humidity: Optional[float] = Field(default=None, alias="humidity")
    precipitation: Optional[float] = Field(default=None, alias="precipitation")
    sun_power: Optional[float] = Field(default=None, alias="sunpower")
    rain_fall_last_24_hour: Optional[float] = Field(
        default=None, alias="rainFallLast24Hour"
    )
    rain_fall_last_hour: Optional[float] = Field(default=None, alias="rainFallLastHour")
    wind_direction_degrees: Optional[int] = Field(
        default=None, alias="winddirectiondegrees"
    )
