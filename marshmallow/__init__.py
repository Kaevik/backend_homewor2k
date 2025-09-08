
class _Field:
    def __init__(self, *args, **kwargs): pass

class fields:
    Int = _Field
    Str = _Field
    Bool = _Field
    Dict = _Field
    List = _Field
    Nested = _Field

class Schema:
    def dump(self, obj):
        def to_plain(o):
            if isinstance(o, (str, int, float, bool)) or o is None:
                return o
            if isinstance(o, dict):
                return {k: to_plain(v) for k, v in o.items()}
            if isinstance(o, (list, tuple, set)):
                return [to_plain(x) for x in o]
            # dataclass or simple object
            if hasattr(o, "__dict__"):
                return {k: to_plain(v) for k, v in o.__dict__.items() if not k.startswith("_")}
            try:
                import dataclasses
                if dataclasses.is_dataclass(o):
                    return {f.name: to_plain(getattr(o, f.name)) for f in dataclasses.fields(o)}
            except Exception:
                pass
            return o
        return to_plain(obj)
