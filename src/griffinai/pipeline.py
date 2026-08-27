from __future__ import annotations

from collections.abc import Iterable

from .domain import ContentBrief, Draft, DraftStatus, PipelineResult
from .ports import ApprovalPolicy, Publisher, TextGenerator, TraceSink


class ContentPipeline:
    """Generate, approve, publish and trace one content job."""

    def __init__(
        self,
        generator: TextGenerator,
        approval: ApprovalPolicy,
        publishers: Iterable[Publisher],
        traces: TraceSink,
    ) -> None:
        self._generator = generator
        self._approval = approval
        self._publishers = tuple(publishers)
        self._traces = traces

    def run(self, brief: ContentBrief) -> PipelineResult:
        brief.validate()
        text = self._generator.generate(brief).strip()
        if not text:
            raise ValueError("generator returned empty content")

        draft = Draft(text=text)
        result = PipelineResult(draft=draft)
        self._traces.record(draft.trace_id, "content.generated", draft_id=draft.id)

        if not self._approval.approve(draft):
            draft.status = DraftStatus.REJECTED
            self._traces.record(draft.trace_id, "content.rejected", draft_id=draft.id)
            return result

        draft.status = DraftStatus.APPROVED
        self._traces.record(draft.trace_id, "content.approved", draft_id=draft.id)

        for publisher in self._publishers:
            try:
                publication = publisher.publish(draft)
                result.publications.append(publication)
                self._traces.record(
                    draft.trace_id,
                    "content.published",
                    channel=publication.channel,
                    external_id=publication.external_id,
                )
            except Exception as error:
                result.errors[publisher.channel] = str(error)
                self._traces.record(
                    draft.trace_id,
                    "content.publish_failed",
                    channel=publisher.channel,
                    error_type=type(error).__name__,
                )

        if result.publications and not result.errors:
            draft.status = DraftStatus.PUBLISHED
        elif result.publications:
            draft.status = DraftStatus.PARTIALLY_PUBLISHED

        return result

