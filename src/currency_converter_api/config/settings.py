from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExchangeRates(BaseModel):
    api_key: str
    latest_rates: HttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")
    exchange_rates: ExchangeRates
