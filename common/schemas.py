from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class FHIRQueryArgs(BaseModel):
    server_url: str
    resource: str
    search: Dict[str, Any] = Field(default_factory=dict)
    include_phis: bool = False
    limit: int = 200

class S3GetArgs(BaseModel):
    bucket: str
    key: str

class VCFParseArgs(BaseModel):
    s3_uri: str
    sample_id: str
    build: str = Field(default="GRCh38")

class TerminologyMapArgs(BaseModel):
    system: str  # SNOMED|LOINC|ICD10|RxNorm|OncoTree
    codes: List[str]

class GEArgs(BaseModel):
    suite: str
    table: str

class SparkJobArgs(BaseModel):
    job: str
    args: Dict[str, Any] = Field(default_factory=dict)

class OPAEvalArgs(BaseModel):
    action: str
    resource: str
    context: Dict[str, Any] = Field(default_factory=dict)

class HITLArgs(BaseModel):
    task_id: str
    summary: str
    diffs: Optional[str] = None

class ToolResult(BaseModel):
    ok: bool
    data: Any = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
