from pydantic import BaseModel

class DatabaseConfig(BaseModel):
  """Database configuration"""

  # The URL of the database to connect to
  url: str

class Config(BaseModel):
  """Root configuration for Shroomery"""

  # Database configuration
  database: DatabaseConfig

def load_config(path: str) -> Config:
  """Load the configuration from a file"""
  with open(path, "r") as f:
    return Config.model_validate_json(f.read())

def load_default_config() -> Config:
  """Load the default configuration"""

  return load_config("/etc/shroomery/config.json")