from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    # MongoDB configs
    MONGO_DATABASE_HOST: str = "mongodb://localhost:27017"
    MONGO_DATABASE_NAME: str = "scrabble"

settings = Settings()
