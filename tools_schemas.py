# tools_schemas.py (Pydantic)
from pydantic import BaseModel, Field
from typing import Optional, List

class FHIRQueryArgs(BaseModel):
    server_url: str
    resource: str = Field(..., description="e.g., 'Patient', 'Observation'")
    search: dict = Field(..., description="FHIR search params")
    include_phis: bool = False

class S3GetArgs(BaseModel):
    bucket: str
    key: str

class VCFParseArgs(BaseModel):
    s3_uri: str
    sample_id: str

class TerminologyMapArgs(BaseModel):
    system: str = Field(..., description="SNOMED|LOINC|ICD10|RxNorm|OncoTree")
    codes: List[str]

class GEArgs(BaseModel):
    suite: str
    table: str

class OPAPolicyArgs(BaseModel):
    action: str
    resource: str
    context: dict  # user role, dataset tags, pii flags

class HITLArgs(BaseModel):
    task_id: str
    summary: str
    diffs: Optional[str] = None
