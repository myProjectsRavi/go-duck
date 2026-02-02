# Template Repo Usage

## One-time: enable template on GitHub
1. Open repo settings.
2. Enable **Template repository**.
3. Save.

## Create a new product repo from this template
1. Click **Use this template** on GitHub.
2. Name the new repo and create it.
3. Add GitHub Actions secrets:
   - JULES_KEY_ARCH
   - JULES_KEY_DEV
   - JULES_KEY_REVIEW
   - JULES_SOURCE (source name, not repo URL)
   - JULES_API_BASE (optional)
4. Install the Jules GitHub App on the new repo.
5. Create an issue and comment with `/agent1 ...` or `/agent1-append ...`.

## Local usage
1. Copy `.env.local.example` to `.env.local`.
2. Run `scripts/run_local.sh`.
