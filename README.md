<div align="center">

# GriffinAI Showcase

### AI content workflow: generation → approval → publishing → tracing

A sanitized, runnable reference implementation inspired by a production content system.

</div>

## About

GriffinAI automates the path from a content brief to publication across several channels. The production system includes LLM agents, scheduled jobs, Telegram/VK/Instagram integrations, media processing, observability and guarded deployment.

This repository is a deliberately isolated showcase. It demonstrates the architectural core without customer data, production credentials, server configuration or proprietary prompts. It does **not** contain the private production source or its Git history.

## What this demo shows

- dependency-inverted LLM and publisher adapters;
- an explicit human approval boundary;
- partial-failure handling for multi-channel publishing;
- correlated workflow tracing;
- deterministic local adapters that need no API keys;
- focused regression tests for the critical workflow.

## Architecture

```text
Content brief
     │
     ▼
TextGenerator ──► Draft ──► ApprovalPolicy
                                │
                    rejected ◄──┴──► approved
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                     Telegram         VK       Instagram
                         └────────────┬────────────┘
                                      ▼
                                  TraceSink
```

The core depends on protocols rather than concrete providers. A real LLM, queue or social network can therefore be added as an adapter without changing the orchestration logic.

## Run locally

Python 3.11 or newer is required.

```bash
python -m venv .venv
```

Activate the environment and install the package:

```bash
python -m pip install -e .
python -m griffinai.demo
```

The demo uses deterministic local adapters and never accesses the network.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover successful publishing, human rejection and isolated provider failure.

## Repository boundaries

The following are intentionally excluded:

- tokens, passwords, cookies and production `.env` files;
- customer content, analytics, databases and logs;
- server addresses, deployment scripts and infrastructure configuration;
- proprietary prompts and platform-specific reverse engineering;
- generated media and third-party API payloads.

Only placeholders belong in `.env.example`. Never commit a populated `.env` file.

## Production case study

The complete private system additionally implements scheduled content generation, reposting between platforms, large-video delivery through a local Telegram Bot API, execution tracing, health checks and rollback-aware deployment.

See the project in the [AI developer portfolio](https://dim-2id.vercel.app/#work).

## Contact

- Telegram: [@dim_2id](https://t.me/dim_2id)
- Email: [agnilisadm@gmail.com](mailto:agnilisadm@gmail.com)

## License

[MIT](LICENSE)

