# FastAPI façade (RBAC/HITL endpoints)
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from orchestration.coordinator import daily_run
from tools.hitl import hitl_decide
from common.schemas import ToolResult


app = FastAPI()

# Root endpoint for health check or welcome message
@app.get("/")
def read_root():
    return {"message": "API is running"}

def user():
    # stub user; integrate with OIDC later
    return {"sub":"u1","roles":["etl_runner","analyst"]}

def require(role: str):
    def dep(u=Depends(user)):
        if role not in u["roles"]:
            raise HTTPException(403, "forbidden")
        return u
    return dep


class DailyIn(BaseModel):
    fhir_url: str
    cohort_tag: str = None


@app.post("/run/daily")
def run_daily(inp: DailyIn, _=Depends(require("etl_runner"))):
    return daily_run(inp.fhir_url, inp.cohort_tag).dict()

class HitlDecision(BaseModel):
    approve: bool

@app.post("/hitl/{task_id}")
def decide(task_id: str, payload: HitlDecision, _=Depends(require("analyst"))):
    return hitl_decide(task_id, payload.approve).dict()
