# OPA policy evaluation (deny by default on unknowns)
from common.schemas import OPAEvalArgs, ToolResult

DEFAULT_RULES = {
    ("export", "external_url"): False,
    ("write", "gold"): True,
    ("delete", "gold"): False,
}

def opa_policy_eval(args: OPAEvalArgs) -> ToolResult:
    key = (args.action, args.resource)
    decision = DEFAULT_RULES.get(key, False)
    return ToolResult(ok=True, data={"allow": decision, "evaluated": key, "context": args.context})
