# VEP / knowledge lookups (stubbed, cacheable)
from common.schemas import ToolResult
from typing import List, Dict

def vep_annotate(variants: List[Dict]) -> ToolResult:
    # Stub: pretend we called VEP and OncoKB
    ann = []
    for v in variants[:100]:  # sample
        ann.append({
            "chrom": v["chrom"], "pos": v["pos"], "ref": v["ref"], "alt": v["alt"],
            "gene": "TP53", "consequence": "missense_variant", 
            "hgvs_p": "p.R175H", "clin_sig": "Pathogenic", "oncogenicity": "Oncogenic"
        })
    return ToolResult(ok=True, data={"n_annotated": len(ann)})
