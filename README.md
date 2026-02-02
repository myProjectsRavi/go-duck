# offline-devs

Three-agent Jules orchestration scaffold for:
- Agent 1: Architect/BA
- Agent 2: Full-stack developer
- Agent 3: Senior code reviewer

## Quick Start
1. Add GitHub Actions secrets:
   - `JULES_KEY_ARCH`
   - `JULES_KEY_DEV`
   - `JULES_KEY_REVIEW`
   - `JULES_SOURCE`
   - `JULES_API_BASE` (optional)
2. Optional env var: `ORCH_STARTING_BRANCH` (defaults to `main`).
3. To submit a product idea via comment, create an issue and comment with one of:
   - `/agent1 ...` (replace backlog)
   - `/agent1-append ...` (append enhancements)
   - `/product ...`
   - `/idea ...`
4. Run the "Orchestrator" workflow with a product prompt, or use the comment intake.
5. Track progress in `status/` and in GitHub Actions logs.

## Local Daytime Runs (to save Actions minutes)
1. Copy `.env.local.example` to `.env.local` and fill in keys.
2. Optionally put your long prompt in a file and set `ORCH_PROMPT_FILE=prompt.txt`.
3. Optional: set `ORCH_AGENT1_MODE=append` for incremental enhancements.
4. Optional: set `ORCH_AUTO_MERGE=true` and `ORCH_MERGE_METHOD=squash`.
5. Run `scripts/run_local.sh`.

## Scheduled Runs (optional)
`Orchestrator Nightly` is manual-only by default. Add a cron schedule in
`.github/workflows/orchestrator-night.yml` if you want automatic runs.

## Docs
- `docs/REPORT.md`
- `docs/RUNBOOK.md`
- `docs/TEMPLATE_SETUP.md`
- `docs/SETUP.md`

## Template Repo (one-click new products)
1. Enable **Template repository** in GitHub settings for this repo.
2. Click **Use this template** to create a new product repo.
3. Add secrets and install the Jules GitHub App in the new repo.
