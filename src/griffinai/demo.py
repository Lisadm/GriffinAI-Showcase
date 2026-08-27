from __future__ import annotations

from .adapters import ConsolePublisher, DemoTextGenerator, KeywordApproval
from .domain import ContentBrief
from .pipeline import ContentPipeline
from .tracing import InMemoryTraceSink


def main() -> None:
    traces = InMemoryTraceSink()
    pipeline = ContentPipeline(
        generator=DemoTextGenerator(),
        approval=KeywordApproval(),
        publishers=[ConsolePublisher("telegram"), ConsolePublisher("vk")],
        traces=traces,
    )
    result = pipeline.run(
        ContentBrief(
            topic="Как AI помогает контент-команде",
            audience="владельцы малого бизнеса",
            tone="экспертно и без лишнего пафоса",
        )
    )

    print(f"\nstatus={result.draft.status}")
    print(f"publications={len(result.publications)} errors={len(result.errors)}")
    print(f"trace_events={len(traces.events)}")


if __name__ == "__main__":
    main()

