from common.schemas import SparkJobArgs, ToolResult
from common.settings import settings

def spark_submit(args: SparkJobArgs) -> ToolResult:
    # For Databricks, call the Jobs API (omitted here); for local, run a python module.
    # We return a fake run-id for now.
    target = f"databricks:{args.job}" if settings.ENV == "databricks" else f"local:{args.job}"
    return ToolResult(ok=True, data={"run_id": f"{target}-12345", "args": args.args})
