from ..config import settings
from ..core.etl.extract import FetchItem, HttpSource
from ..core.etl.pipeline import Pipeline
from ..core.etl.transform import (
    DictToPydanticTransformer,
    FromJsonToEntryTransformer,
    PydanticToPydanticTransformer,
)
from ..models import Measurement, WeatherStation
from .schema import StationMeasurement


class BuienradarPipeline:
    """The complete pipeline to load buienradar data"""

    def run(self) -> None:
        json_transformer = FromJsonToEntryTransformer(("actual", "stationmeasurements"))

        transform_to_schema = DictToPydanticTransformer(StationMeasurement)

        source = HttpSource(url=settings.source_url)
        initial_pipeline: Pipeline[FetchItem] = Pipeline(source)
        base_pipeline = initial_pipeline.add(json_transformer).add(transform_to_schema)

        weather_station_transformer = PydanticToPydanticTransformer(
            StationMeasurement,
            WeatherStation,
            self.transform_data_to_weather_station,
        )
        measurement_transformer = PydanticToPydanticTransformer(
            StationMeasurement, Measurement, self.transform_data_to_measurement
        )
        wheather_station_pipeline = base_pipeline.add(weather_station_transformer)
        measurement_pipeline = base_pipeline.add(measurement_transformer)

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
