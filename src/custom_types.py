from typing import Dict, NewType

Action = NewType("Action", dict(type=str, params=dict(value=str)))
FlowData = NewType("FlowData", dict(key_type=str, key=str, step=str, percentage=int, action=Action))
