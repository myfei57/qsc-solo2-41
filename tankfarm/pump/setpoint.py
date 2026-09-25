"""Pump setpoint and ramp handling."""

from __future__ import annotations

from tankfarm.errors import NegativeSetpointError
from tankfarm.pump.arbiter import HeaderArbiter
from tankfarm.pump.model import Pump


class SetpointController:
    """Applies setpoints directly or in a single move to the target."""

    def __init__(self, arbiter: HeaderArbiter) -> None:
        self._arbiter = arbiter

    def apply(self, pump: Pump, value: float) -> float:
        if value < 0:
            raise NegativeSetpointError(value)
        pump.setpoint = float(value)
        return self._arbiter.write(pump.pump_id, value)

    def ramp(self, pump: Pump, target: float) -> tuple[float, ...]:
        if target < 0:
            raise NegativeSetpointError(target)
        if target == pump.setpoint:
            return ()
        return (self.apply(pump, target),)
