from typing import Dict, NewType

Action = NewType("Action", dict(type=str, params=Dict))
FlowData = NewType("FlowData", dict(key_type=str, key=str, step=str, percentage=int, action=Action))
