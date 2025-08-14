# agents/qc.py
from common.schemas import GEArgs
from tools.ge_runner import great_expectations_run

def run_silver_checks(table: str):
    return great_expectations_run(GEArgs(suite="onc_silver", table=table))
