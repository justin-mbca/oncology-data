# Agents (thin wrappers around tools)
from common.schemas import FHIRQueryArgs, ToolResult
from tools.fhir_client import fhir_query
from tools.s3_io import s3_list



from datetime import datetime, timedelta

def pull_daily_observations(server_url: str, cohort_tag: str = None) -> ToolResult:
    # Use a valid FHIR _lastUpdated filter (e.g., gt2025-08-13T00:00:00Z)
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    search = {"_lastUpdated": f"gt{yesterday}"}
    if cohort_tag:
        search["_tag"] = cohort_tag
    args = FHIRQueryArgs(server_url=server_url, resource="Observation", search=search)
    return fhir_query(args)

def discover_genomics(prefix_uri: str) -> ToolResult:
    return s3_list(prefix_uri)
