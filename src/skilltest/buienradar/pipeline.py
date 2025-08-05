from ..config import settings
from ..core.extract import FetchItem, HttpSource
from ..core.pipeline import Pipeline
from ..core.transform import (
    DictToPydanticTransformer,
    FromJsonToEntryTransformer,
    PydanticToPydanticTransformer,
)
from ..models import Measurement, WeatherStation
from .schema import StationMeasurement


class BuienradarPipeline:
    """The complete pipeline to load buienradar data"""

    def run(self) -> None:
        source = HttpSource(url=settings.source_url)
        initial_pipeline: Pipeline[FetchItem] = Pipeline(source)
        base_pipeline = initial_pipeline.add(
            FromJsonToEntryTransformer(("actual", "stationmeasurements"))
        ).add(DictToPydanticTransformer(StationMeasurement))

        wheather_station_pipeline = base_pipeline.add(
            PydanticToPydanticTransformer(
                StationMeasurement,
                WeatherStation,
                self.transform_data_to_weather_station,
            )
        )
        measurement_pipeline = base_pipeline.add(
            PydanticToPydanticTransformer(
                StationMeasurement, Measurement, self.transform_data_to_measurement
            )
        )

        # as an improvement the common functionality of these pipelines can be merged in the execution stage
        wheather_station_pipeline.run()
        measurement_pipeline.run()

    @staticmethod
    def transform_data_to_weather_station(input: StationMeasurement) -> WeatherStation:
        return WeatherStation(
            stationid=input.station_id,
            stationname=input.station_name,
            lat=input.lat,
            lon=input.lon,
            regio=input.regio,
        )

    @staticmethod
    def transform_data_to_measurement(input: StationMeasurement) -> Measurement:
        return Measurement(
            timestamp=input.timestamp,
            temperature=input.temperature,
            groundtemperature=input.ground_temperature,
            feeltemperature=input.feel_temperature,
            windgusts=input.wind_gusts,
            windspeedBft=input.wind_speed_bft,
            humidity=input.humidity,
            precipitation=input.precipitation,
            sunpower=input.sun_power,
            stationid=input.station_id,
        )
