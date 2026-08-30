from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    CITY_NAME: str = "Mangaluru"

    DEPOT_LAT: float = 12.9141
    DEPOT_LNG: float = 74.8560

    DEFAULT_BIN_CAPACITY: float = 1000
    DEFAULT_TRUCK_CAPACITY: float = 5000

    class Config:
        env_file = ".env"


settings = Settings()