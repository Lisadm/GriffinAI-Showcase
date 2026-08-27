from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class TraceEvent:
    trace_id: str
    event: str
    attributes: dict[str, object]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class InMemoryTraceSink:
    """Small observable trace sink used by the demo and tests."""

    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def record(self, trace_id: str, event: str, **attributes: object) -> None:
        self.events.append(TraceEvent(trace_id, event, attributes))

