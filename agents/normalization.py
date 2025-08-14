# agents/normalization.py
from common.schemas import TerminologyMapArgs
from tools.terminology import terminology_map

def normalize_loinc(codes):
    return terminology_map(TerminologyMapArgs(system="LOINC", codes=codes))
