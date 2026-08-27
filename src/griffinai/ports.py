from __future__ import annotations

from typing import Protocol

from .domain import ContentBrief, Draft, PublishResult


class TextGenerator(Protocol):
    def generate(self, brief: ContentBrief) -> str: ...


class ApprovalPolicy(Protocol):
    def approve(self, draft: Draft) -> bool: ...


class Publisher(Protocol):
    @property
    def channel(self) -> str: ...

    def publish(self, draft: Draft) -> PublishResult: ...


class TraceSink(Protocol):
    def record(self, trace_id: str, event: str, **attributes: object) -> None: ...

