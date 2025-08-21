import httpx
from sqlmodel import Session

from .config import settings
from .database import engine
from .models import Measurement, WeatherStation


def load_data():
    """Load weather data from API and persist to database."""
    response = httpx.get(settings.source_url)
    response.raise_for_status()
    data = response.json()["actual"]["stationmeasurements"]

    with Session(engine) as session:
        for entry in data:
            session.merge(WeatherStation.model_validate(entry))
            session.merge(Measurement.model_validate(entry))

        session.commit()
