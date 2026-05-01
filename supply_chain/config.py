from dataclasses import dataclass
import os

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///supply_chain.db")

settings = Settings()
