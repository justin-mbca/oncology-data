# FHIR client (read-only, server-side filtering)

import requests
from typing import Dict, Any, List
from common.schemas import FHIRQueryArgs, ToolResult
from common.redaction import safe_log_payload
from common.settings import settings

def fhir_query(args: FHIRQueryArgs) -> ToolResult:
    headers = {"Authorization": f"Bearer {settings.FHIR_TOKEN}"} if settings.FHIR_TOKEN else {}
    params = args.search.copy()
    params["_count"] = args.limit
    # Only include _elements if it is set and non-empty
    if params.get("_elements"):
        params["_elements"] = params["_elements"]
    elif "_elements" in params:
        del params["_elements"]
    url = f"{args.server_url.rstrip('/')}/{args.resource}"
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        bundle = r.json()
        # Return only pointers (no raw PHI in logs)
        entries = bundle.get("entry", [])
        pointers = [{"resourceType": e["resource"]["resourceType"],
                     "id": e["resource"].get("id")} for e in entries if "resource" in e]
        return ToolResult(ok=True, data=bundle, meta={"pointers": pointers, "log": safe_log_payload(pointers)})
    except Exception as e:
        return ToolResult(ok=False, error=str(e))
