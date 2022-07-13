"""
Taken from: https://github.com/aprilahijriyan/falca/blob/main/falca/compat.py
"""

from functools import partial

from pydantic import BaseModel


def _json_default(o: object):
    if isinstance(o, BaseModel):
        return o.dict()
    raise ValueError(f"unknown object {o!r}")


try:
    import orjson as json

    _dumps = json.dumps

    def dumps(*args, **kwds):
        option = kwds.get("option")
        if not option:
            option = json.OPT_NON_STR_KEYS
        kwds["option"] = option
        return _dumps(*args, **kwds)

except ImportError:  # pragma: no cover
    try:
        import rapidjson as json

        dumps = json.dumps

    except ImportError:
        import json

        dumps = json.dumps

dump = getattr(json, "dump", None)
load = getattr(json, "load", None)
loads = json.loads
dumps = partial(dumps, default=_json_default)
