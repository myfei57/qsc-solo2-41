"""Header setpoint arbitration between pumps."""

from __future__ import annotations

from typing import Any

from tankfarm.errors import NegativeSetpointError
from tankfarm.valve.header import Header


class HeaderArbiter:
    """Keeps the latest demand and writes through to the header."""

    def __init__(self, header: Header) -> None:
        self._header = header
        self._last_writer = ""
        self._demand = 0.0

    def write(self, pump_id: str, value: float) -> float:
        if value < 0:
            raise NegativeSetpointError(value)
        self._last_writer = pump_id
        self._demand = float(value)
        return self._header.write(value)

    def value(self) -> float:
        return self._header.setpoint()

    def last_writer(self) -> str:
        return self._last_writer

    def demands(self) -> dict[str, float]:
        if not self._last_writer:
            return {}
        return {self._last_writer: self._demand}

    def as_payload(self) -> dict[str, Any]:
        return {
            "setpoint": self.value(),
            "last_writer": self.last_writer(),
            "demands": self.demands(),
        }
