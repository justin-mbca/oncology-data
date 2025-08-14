from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = Field(default="local", description="local|databricks")
    S3_ENDPOINT: str = ""
    S3_BUCKET: str = ""
    FHIR_BASE_URL: str = "https://hapi.fhir.org/baseR4"
    FHIR_TOKEN: str = ""
    OPENLINEAGE_URL: str = ""
    OPA_URL: str = ""
    DBT_PROJECT_DIR: str = "transforms/dbt_project"
    DELTA_ROOT: str = "data"  # local path or s3://bucket/prefix
    HITL_DB: str = "hitl.sqlite"
    # Databricks (optional)
    DATABRICKS_HOST: str = ""
    DATABRICKS_TOKEN: str = ""
    DATABRICKS_CLUSTER_ID: str = ""

settings = Settings()
