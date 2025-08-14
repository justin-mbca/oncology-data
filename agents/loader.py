# agents/loader.py
from common.schemas import SparkJobArgs
from tools.spark_exec import spark_submit
from tools.lineage import openlineage_emit

def build_gold_variants():
    r = spark_submit(SparkJobArgs(job="dbt_run", args={"select":"models/gold/variants.sql"}))
    openlineage_emit({"run_id": r.data.get("run_id"), "status": "COMPLETED"})
    return r
