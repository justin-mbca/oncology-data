# Orchestration (one function to call)
from agents.ingestion import pull_daily_observations, discover_genomics
from agents.normalization import normalize_loinc
from agents.genomics import parse_and_annotate_vcf
from agents.qc import run_silver_checks
from agents.loader import build_gold_variants

from tools.hitl import hitl_queue
from common.schemas import ToolResult, HITLArgs


def daily_run(fhir_url: str, cohort_tag: str = None) -> ToolResult:
    obs = pull_daily_observations(fhir_url, cohort_tag)
    if not obs.ok:
        return obs

    # pretend we extracted LOINC codes
    loincs = ["718-7", "6690-2", "9999-9"]
    norm = normalize_loinc(loincs)
    qc = run_silver_checks("silver.observation")


    # genomics discovery + process one sample
    g = discover_genomics("s3://genomics/drop/")
    # use the downloaded test VCF file
    anno = parse_and_annotate_vcf("s3://genomics/drop/test.vcf", "TEST_SAMPLE")

    # require HITL before any external export

    hitl_queue_id = f"export-{cohort_tag}" if cohort_tag else "export"
    hitl = hitl_queue(HITLArgs(task_id=hitl_queue_id, summary="Approve limited dataset export?", diffs="Added 123 records."))

    gold = build_gold_variants()
    return ToolResult(ok=True, data={
        "observations": obs.meta, "norm": norm.data, "qc": qc.data,
        "genomics": anno.data, "hitl": hitl.data, "gold": gold.data
    })
