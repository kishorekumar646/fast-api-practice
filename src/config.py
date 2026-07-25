from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./my-bookstore.db"
    JWT_SECRET: str = "your_jwt_secret_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRY: int = 3600      # 1 hour
    REFRESH_TOKEN_EXPIRY: int = 604800   # 7 days
    REDIS_URL: str = "redis://localhost:6379/0"
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


Config: Settings = Settings()
