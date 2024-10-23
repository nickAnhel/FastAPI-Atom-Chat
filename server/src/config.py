from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    title: str = "Atom Chat"
    version: str = "0.1.0"
    description: str = "Test task for the Backend trainee developer vacancy in Rosatom"
    debug: bool = True


class DBSettings(BaseSettings):
    DB_MODE: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ECHO: bool

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".test.env", extra="ignore")


class Settings(BaseSettings):
    project: ProjectSettings = ProjectSettings()
    database: DBSettings = DBSettings()  # type: ignore


settings = Settings()
