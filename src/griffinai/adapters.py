from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .domain import ContentBrief, Draft, PublishResult


class DemoTextGenerator:
    """Deterministic local generator: no network calls or credentials."""

    def generate(self, brief: ContentBrief) -> str:
        return (
            f"{brief.topic}\n\n"
            f"Материал для аудитории: {brief.audience}. "
            f"Тон публикации: {brief.tone}.\n\n"
            "Это демонстрационный текст. Подключите LLM-адаптер через TextGenerator, "
            "не меняя orchestration pipeline."
        )


@dataclass(slots=True)
class KeywordApproval:
    """Represents a human approval boundary in a deterministic demo."""

    forbidden_terms: tuple[str, ...] = ("secret", "password", "token")

    def approve(self, draft: Draft) -> bool:
        normalized = draft.text.casefold()
        return not any(term.casefold() in normalized for term in self.forbidden_terms)


class ConsolePublisher:
    def __init__(self, channel: str) -> None:
        self._channel = channel

    @property
    def channel(self) -> str:
        return self._channel

    def publish(self, draft: Draft) -> PublishResult:
        digest = sha256(f"{self.channel}:{draft.id}".encode()).hexdigest()[:12]
        print(f"[{self.channel}] {draft.text}")
        return PublishResult(channel=self.channel, external_id=digest)

