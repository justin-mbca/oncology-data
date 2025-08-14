# OpenLineage emitter (audit)
from common.schemas import ToolResult
from common.settings import settings

def openlineage_emit(run: dict) -> ToolResult:
    # send to OpenLineage (stub)
    return ToolResult(ok=True, data={"sent": True, "to": settings.OPENLINEAGE_URL})
