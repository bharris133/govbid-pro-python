from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, Any
from datetime import datetime

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "me@$1Tim3"  # In production, use a secure random key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./govbid_pro.db"
    PROJECT_NAME: str = "GovBid Pro"
    PROJECT_DESCRIPTION: str = "Proposal writer for government contracts"
    VERSION: str = "1.0.0"  # Add the VERSION attribute
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000", "http://localhost:3000"]
    
    # Superuser settings
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    
    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    model_config = ConfigDict(case_sensitive=True)

settings = Settings()
