import re

EXCLUDE_PATTERNS = (
    r".*/\.git(/|$)",
    r".*/__pycache__(/|$)",
    r".*/__pypackages__(/|$)",
    r".*\.egg-info(/|$)",
    r".*/\.mypy_cache(/|$)",
    r".*/School(/|$)",
)


def excluded(path):
    for pattern in EXCLUDE_PATTERNS:
        if re.match(pattern, path):
            return True
    return False
