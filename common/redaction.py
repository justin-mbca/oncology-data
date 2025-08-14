import re

PHI_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN (US) example
    re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),  # phone
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),  # full DOB yyyy-mm-dd (treat with care)
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
]

def redact(text: str) -> str:
    s = str(text)
    for pat in PHI_PATTERNS:
        s = pat.sub("[REDACTED]", s)
    return s

def safe_log_payload(payload):
    # Never log raw resources; return sizes and hashes only.
    try:
        from hashlib import sha256
        b = str(payload).encode("utf-8")
        return {"sha256": sha256(b).hexdigest(), "length": len(b)}
    except Exception:
        return {"info": "unloggable"}
