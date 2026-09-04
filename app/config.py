#app/config.py
import os
import dotenv

dotenv.load_dotenv()

class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    POSTGRES_URL = (f"postgresql+asyncpg://"
                    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
                    )

config = Config()