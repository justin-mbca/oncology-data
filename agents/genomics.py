# agents/genomics.py
from common.schemas import VCFParseArgs, ToolResult
from tools.vcf_parse import vcf_parse
from tools.vep import vep_annotate

def parse_and_annotate_vcf(s3_uri: str, sample_id: str, build="GRCh38") -> ToolResult:
    parsed = vcf_parse(VCFParseArgs(s3_uri=s3_uri, sample_id=sample_id, build=build))
    if not parsed.ok: return parsed
    # In a real run, fetch rows from bronze; here we pass a small fake set
    fake_rows = [{"chrom":"17","pos":7673803,"ref":"C","alt":"T"}] * 10
    return vep_annotate(fake_rows)
