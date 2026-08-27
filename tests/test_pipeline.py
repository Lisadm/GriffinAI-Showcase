from __future__ import annotations

import unittest

from griffinai.domain import ContentBrief, DraftStatus, PublishResult
from griffinai.pipeline import ContentPipeline
from griffinai.tracing import InMemoryTraceSink


class StubGenerator:
    def __init__(self, text: str) -> None:
        self.text = text

    def generate(self, brief: ContentBrief) -> str:
        return self.text


class FixedApproval:
    def __init__(self, approved: bool) -> None:
        self.approved = approved

    def approve(self, draft: object) -> bool:
        return self.approved


class RecordingPublisher:
    def __init__(self, channel: str, *, fail: bool = False) -> None:
        self._channel = channel
        self.fail = fail
        self.calls = 0

    @property
    def channel(self) -> str:
        return self._channel

    def publish(self, draft: object) -> PublishResult:
        self.calls += 1
        if self.fail:
            raise RuntimeError("provider unavailable")
        return PublishResult(self.channel, f"{self.channel}-42")


class ContentPipelineTests(unittest.TestCase):
    def test_approved_content_is_published_and_traced(self) -> None:
        traces = InMemoryTraceSink()
        telegram = RecordingPublisher("telegram")
        pipeline = ContentPipeline(
            StubGenerator("Ready to publish"),
            FixedApproval(True),
            [telegram],
            traces,
        )

        result = pipeline.run(ContentBrief("AI agents", "product teams"))

        self.assertEqual(DraftStatus.PUBLISHED, result.draft.status)
        self.assertEqual(1, telegram.calls)
        self.assertEqual(["content.generated", "content.approved", "content.published"], [e.event for e in traces.events])

    def test_rejected_content_never_reaches_publishers(self) -> None:
        publisher = RecordingPublisher("telegram")
        pipeline = ContentPipeline(
            StubGenerator("Needs review"),
            FixedApproval(False),
            [publisher],
            InMemoryTraceSink(),
        )

        result = pipeline.run(ContentBrief("Draft", "editors"))

        self.assertEqual(DraftStatus.REJECTED, result.draft.status)
        self.assertEqual(0, publisher.calls)

    def test_one_provider_failure_does_not_lose_other_publications(self) -> None:
        pipeline = ContentPipeline(
            StubGenerator("Publish everywhere"),
            FixedApproval(True),
            [RecordingPublisher("telegram"), RecordingPublisher("instagram", fail=True)],
            InMemoryTraceSink(),
        )

        result = pipeline.run(ContentBrief("Release", "customers"))

        self.assertEqual(DraftStatus.PARTIALLY_PUBLISHED, result.draft.status)
        self.assertEqual(["telegram"], [item.channel for item in result.publications])
        self.assertEqual({"instagram": "provider unavailable"}, result.errors)


if __name__ == "__main__":
    unittest.main()

