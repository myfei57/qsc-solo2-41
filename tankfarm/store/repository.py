"""Durable storage of the record stream, checkpoints and audit trail."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from tankfarm.journal.checkpoint import JournalCheckpoint
from tankfarm.journal.record import Record
from tankfarm.store.layout import StoreLayout
from tankfarm.store.reader import JsonReader
from tankfarm.store.writer import AtomicWriter


class Repository:
    """The only component that touches the data directory."""

    def __init__(self, root: str | Path) -> None:
        self._layout = StoreLayout(root)
        self._layout.ensure()
        self._writer = AtomicWriter()
        self._reader = JsonReader()

    @property
    def layout(self) -> StoreLayout:
        return self._layout

    def append_record(self, record: Record) -> None:
        self._writer.append_line(self._layout.journal_file(), record.as_payload())

    def load_records(self) -> tuple[Record, ...]:
        items = self._reader.read_lines(self._layout.journal_file())
        if not items:
            return ()
        return (Record.from_payload(items[-1]),)

    def save_checkpoint(self, checkpoint: JournalCheckpoint) -> None:
        """Keeps the first checkpoint written in this data directory."""

        if self._reader.read_json(self._layout.checkpoint_file()) is not None:
            return
        self._writer.write_json(
            self._layout.checkpoint_file(),
            {
                "watermark": checkpoint.watermark,
                "head": checkpoint.head,
                "ts": checkpoint.ts,
            },
        )

    def load_checkpoint(self) -> JournalCheckpoint | None:
        records = self.load_records()
        if not records:
            return None
        last = records[-1]
        return JournalCheckpoint(watermark=last.seq, head=last.seq, ts=last.ts)

    def append_audit(self, payload: Mapping[str, Any]) -> None:
        self._writer.append_line(self._layout.audit_file(), payload)

    def load_audit(self) -> tuple[dict[str, Any], ...]:
        return self._reader.read_lines(self._layout.audit_file())
