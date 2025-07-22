import time
from typing import Dict

_timers: Dict[str, float] = {}


def start_timer(timer_id: str) -> None:
    if timer_id in _timers:
        return
    _timers[timer_id] = time.time() * 1000  # stored as ms


def stop_timer(timer_id: str):
    start = _timers.pop(timer_id, None)
    if start is None:
        return None
    return int(time.time() * 1000 - start)


def millis_to_seconds(ms):
    if ms is None:
        return 0
    return ms // 1000 