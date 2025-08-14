# agents/safety.py
from tools.opa_client import opa_policy_eval
from common.schemas import OPAEvalArgs

def guard_export(target: str, requester: str):
    return opa_policy_eval(OPAEvalArgs(action="export", resource="external_url", context={"user": requester, "target": target}))
