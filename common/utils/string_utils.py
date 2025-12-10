from typing import Any
import json


def to_pretty_str(data:Any):
    return json.dumps(data, indent=2, ensure_ascii=False)