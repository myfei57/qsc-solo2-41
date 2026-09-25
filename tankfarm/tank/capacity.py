"""Remaining volume estimation from calibrated readings."""

from __future__ import annotations

from tankfarm.level.service import LevelService
from tankfarm.tank.registry import TankRegistry


class CapacityEstimator:
    """Turns a raw reading into the headroom left in a tank."""

    def __init__(self, tanks: TankRegistry, levels: LevelService) -> None:
        self._tanks = tanks
        self._levels = levels

    def net_volume(self, tank_id: str) -> float:
        state = self._levels.state(tank_id)
        return state.reading - state.offset

    def remaining(self, tank_id: str) -> float:
        tank = self._tanks.get(tank_id)
        return tank.capacity_mm - self._levels.state(tank_id).reading
