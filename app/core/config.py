from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./app.db"
    aic_base_url: str = "https://api.artic.edu/api/v1"
    aic_timeout_seconds: float = 5.0

    basic_auth_enabled: bool = False
    basic_auth_username: str = "admin"
    basic_auth_password: str = "admin"

settings = Settings()
