from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    source_url: str = "https://data.buienradar.nl/2.0/feed/json"
    database_url: str = "sqlite:///weather_data.db"
    echo_sql: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
