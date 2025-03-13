from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", case_sensitive=False)

    name: str = Field(default="AlertM", alias="APP_NAME")
    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=5005, alias="APP_PORT")
    workers: int = Field(default=4, alias="APP_WORKERS")
    api_key: str = Field(..., alias="API_KEY")