# S3/ADLS IO (local or real)
import os, json
from urllib.parse import urlparse
from common.schemas import S3GetArgs, ToolResult
from common.settings import settings

def _resolve(uri: str) -> str:
    if uri.startswith("s3://") or uri.startswith("abfss://"):
        # For a quick local start, map to local folder
        return os.path.join(settings.DELTA_ROOT, uri.split("://",1)[1].replace("/", "_"))
    return uri

def s3_get(args: S3GetArgs) -> ToolResult:
    # Local stub: read from DELTA_ROOT/bucket_key
    local_path = _resolve(f"s3://{args.bucket}/{args.key}")
    try:
        with open(local_path, "rb") as f:
            b = f.read(256)  # don't return full content
        return ToolResult(ok=True, data={"preview_bytes": len(b)}, meta={"path": local_path})
    except Exception as e:
        return ToolResult(ok=False, error=str(e))

def s3_list(prefix_uri: str) -> ToolResult:
    # Very simple local listing
    path = _resolve(prefix_uri)
    base = os.path.dirname(path)
    try:
        files = [x for x in os.listdir(base) if x.startswith(os.path.basename(path))]
        return ToolResult(ok=True, data={"files": files}, meta={"base": base})
    except Exception as e:
        return ToolResult(ok=False, error=str(e))
