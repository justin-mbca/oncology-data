# Terminology mapping (deterministic rules + stubs)
from common.schemas import TerminologyMapArgs, ToolResult

FAKE_MAPS = {
    "LOINC": {"718-7": "Hemoglobin", "6690-2": "Leukocytes [#/volume] in Blood"},
    "OncoTree": {"BRCA": "Breast", "LUAD": "Lung Adenocarcinoma"}
}

def terminology_map(args: TerminologyMapArgs) -> ToolResult:
    mapped = {c: FAKE_MAPS.get(args.system, {}).get(c, None) for c in args.codes}
    unknown = [c for c, v in mapped.items() if v is None]
    return ToolResult(ok=True, data={"mapped": mapped, "unknown": unknown})
