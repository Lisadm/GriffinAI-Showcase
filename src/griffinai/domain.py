from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class DraftStatus(StrEnum):
    GENERATED = "generated"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    PARTIALLY_PUBLISHED = "partially_published"


@dataclass(frozen=True, slots=True)
class ContentBrief:
    topic: str
    audience: str
    tone: str = "clear and friendly"

    def validate(self) -> None:
        if not self.topic.strip():
            raise ValueError("topic must not be empty")
        if not self.audience.strip():
            raise ValueError("audience must not be empty")


@dataclass(slots=True)
class Draft:
    text: str
    id: str = field(default_factory=lambda: str(uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    status: DraftStatus = DraftStatus.GENERATED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class PublishResult:
    channel: str
    external_id: str


@dataclass(slots=True)
class PipelineResult:
    draft: Draft
    publications: list[PublishResult] = field(default_factory=list)
    errors: dict[str, str] = field(default_factory=dict)

