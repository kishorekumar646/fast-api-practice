from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    JWT_SECRET: str = "your_jwt_secret"
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str = "your_email@example.com"
    DOMAIN: str = "localhost"
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

Config: Settings = Settings()

broker_url = Config.REDIS_URL
resutl_backend = Config.REDIS_URL