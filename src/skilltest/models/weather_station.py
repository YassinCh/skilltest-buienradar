from sqlmodel import Field, SQLModel


class WeatherStation(SQLModel, table=True):
    stationid: int = Field(primary_key=True)
    stationname: str
    lat: float
    lon: float
    regio: str
