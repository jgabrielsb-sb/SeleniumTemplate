from pydantic_settings import (
    BaseSettings,
)

from dotenv import load_dotenv

load_dotenv(override=True)
    
class Settings(BaseSettings):
    pass
    
    
settings = Settings()
    
    
    