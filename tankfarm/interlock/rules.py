"""Set and clear conditions of every latch."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

OVERFILL_LATCH = "overfill"
BLANKET_LATCH = "blanket"


@dataclass(frozen=True)
class ControlContext:
    """Everything the latch rules are allowed to look at."""

    level_overfilled: bool
    gauge_confirmed: bool
    blanket_alarm: bool
    blanket_confirmed: bool


@dataclass(frozen=True)
class LatchRule:
    name: str
    description: str
    set_when: Callable[[ControlContext], bool]


def _overfill_set(ctx: ControlContext) -> bool:
    return ctx.level_overfilled and ctx.gauge_confirmed


def _blanket_set(ctx: ControlContext) -> bool:
    return ctx.blanket_alarm


OVERFILL_RULE = LatchRule(
    name=OVERFILL_LATCH,
    description="level reached the high limit while the gauge was confirmed",
    set_when=_overfill_set,
)

BLANKET_RULE = LatchRule(
    name=BLANKET_LATCH,
    description="blanket gas pressure left its window",
    set_when=_blanket_set,
)


def default_rules() -> tuple[LatchRule, ...]:
    return (OVERFILL_RULE, BLANKET_RULE)
