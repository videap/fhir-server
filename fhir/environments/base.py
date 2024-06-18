import os
from typing import Literal
from nanosettings import NanoSettings, cached_settings, SettingsConfigDict, BaseSettings
from nanosettings.components import Secret

class Settings(NanoSettings):

    app_name: str = "fhir"
    env:str = os.environ["ENV"]
    project_id: str = ""
    log_level: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] = "INFO"
    production: bool
    proxied: bool

    model_config = SettingsConfigDict(env_file=f"fhir/environments/.{os.environ["ENV"]}.env", env_prefix="fhir_")


def get_settings() -> Settings:
    return cached_settings(cls=Settings) #type: ignore