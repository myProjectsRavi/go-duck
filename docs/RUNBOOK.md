# Runbook

## Day-0 Setup
1. Install the Jules GitHub app on this repo.
2. Create three Jules API keys (Architect, Dev, Reviewer).
3. Add GitHub Actions secrets:
   - JULES_KEY_ARCH
   - JULES_KEY_DEV
   - JULES_KEY_REVIEW
   - JULES_SOURCE
   - (Optional) JULES_API_BASE
4. (Optional) Set ORCH_STARTING_BRANCH if your default branch is not main.
5. Commit the orchestrator code and workflow.

## Day-1 Usage
1. Option A: GitHub comment intake
   - Create an issue and comment with `/agent1 ...` (replace) or `/agent1-append ...` (enhancements).
   - The workflow triggers automatically on the comment.
2. Option B: Manual workflow dispatch
   - Go to GitHub Actions and run the "Orchestrator" workflow.
   - Provide a product prompt in the workflow input field.
3. Track progress in Actions logs and `status/` files.
4. Review PRs and follow Agent 3 verdicts.

## Recovery
- If a run fails, check `status/last_error.json` for context.
- Re-run the workflow to resume.
