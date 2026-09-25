"""Query filters shared by the audit trail and the record stream."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class RecordFilter:
    """Narrows a record set by kind, subject, sequence window and limit."""

    kinds: tuple[str, ...] = ()
    subject: str | None = None
    min_seq: int = 0
    max_seq: int = 0
    limit: int = 0

    def matches(self, record: Any) -> bool:
        if self.kinds and record.kind not in self.kinds:
            return False
        if self.min_seq and record.seq < self.min_seq:
            return False
        if self.max_seq and record.seq > self.max_seq:
            return False
        return True

    def apply(self, records: Sequence[Any]) -> tuple[Any, ...]:
        return tuple(record for record in records if self.matches(record))

    def as_payload(self) -> dict[str, Any]:
        return {
            "kinds": list(self.kinds),
            "subject": self.subject,
            "min_seq": self.min_seq,
            "max_seq": self.max_seq,
            "limit": self.limit,
        }
