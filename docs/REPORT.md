# Multi-Agent Orchestrator Report (Draft)

## 1. Executive Summary
This repository implements a zero-infra, zero-DB, repo-as-state orchestration system that coordinates three AI agents:
- Agent 1: Architect + Business Analyst (intake, architecture, epics/features/stories)
- Agent 2: Full-Stack Developer (implements a feature in a single PR)
- Agent 3: Senior Code Reviewer (verifies changes and requests fixes)

The orchestrator is intended to run in GitHub Actions, using three Jules API keys (one per agent) and a single GitHub repo as the system of record.

## 2. Roles and Responsibilities
### Agent 1 (Architect/BA)
- Receives raw product prompt from the product owner.
- Produces backlog artifacts: epics, features, stories, acceptance criteria.
- Outputs structured YAML so the orchestrator can ingest and validate.

### Agent 2 (Developer)
- Takes the next ready feature.
- Implements all stories for that feature in one PR.
- Reports completion to Agent 1 via structured output and status updates.

### Agent 3 (Reviewer)
- Reviews the PR against acceptance criteria, security, and performance.
- Returns PASS or NEEDS_CHANGES with blocking issues first.
- Triggers a fix loop if required.

## 3. High-Level Architecture
- Orchestrator runs on GitHub Actions (no servers).
- State is stored in repo YAML/JSON (no database).
- Each agent uses a separate Jules session and API key.
- Developer sessions use automation mode to auto-create PRs.

## 4. Core Flow (Single Product)
1. Product owner provides a prompt through workflow dispatch input.
   - Or via issue comment (prefix `/agent1`, `/product`, or `/idea`).
2. Orchestrator starts Agent 1 session and parses backlog output.
3. Orchestrator selects next ready feature.
4. Agent 2 implements feature in a single PR.
5. Agent 3 reviews the PR and decides PASS/NEEDS_CHANGES.
6. If NEEDS_CHANGES, Agent 2 fixes and Agent 3 re-reviews.
7. Status files are updated; completion is reported.

## 5. Backlog Data Model
Backlog files are stored under `backlog/`:
- `product.yaml`
- `epics.yaml`
- `features.yaml`
- `stories.yaml`
- `acceptance.yaml`

All backlog files use the same schema shape:
- `version`: integer
- `items`: list of objects (except `product.yaml`)

## 6. State Machine
Product:
- draft -> active -> shipped

Epic:
- planned -> in_progress -> done

Feature:
- ready -> in_progress -> review -> done

Story:
- ready -> in_progress -> done -> verified

The orchestrator enforces transitions and prevents skipping review.

## 7. Security Model
- Jules API keys live only in GitHub Actions secrets.
- Workflows are triggered by manual dispatch or schedule.
- No PR-triggered workflows that expose secrets to forks.
- Minimal GitHub permissions (contents, pull-requests, issues).

## 8. Cost Model
- GitHub Actions free minutes are the only hard quota.
- A concurrency guard limits simultaneous runs.
- Timeouts and circuit breakers prevent runaway usage.

## 9. Failure Handling
- All errors are written to `status/last_error.json`.
- The run is idempotent; it resumes from the last known state.
- If a session fails, the orchestrator stops and awaits retry.

## 10. Implementation Notes
- The orchestrator is written in Python.
- Minimal dependencies: `requests` and `PyYAML`.
- GitHub Actions runs `python -m orchestrator.run`.

## 11. Limitations
- The Jules API is external and versioned; drift risk exists.
- Full "fire-and-forget" is constrained by API changes and quota caps.

## 12. Next Steps
- Run initial workflow with a sample product prompt.
- Validate backlog output and state transitions.
- Enable branch protection when ready.
 - Use `status/product_status.json` for epic/feature counts.
