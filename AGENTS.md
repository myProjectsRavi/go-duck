# AGENTS.md

## Project: Zero-Scout

**Vision:** A "Fire and Forget" market intelligence tool.

## The Iron Triangle of Constraints
Any deviation requires direct approval.

1.  **Zero Auth:** No database, no user accounts. Stateless session only.
2.  **Zero Paid APIs:** Rely solely on `duckduckgo-search`. No Google/Bing APIs.
3.  **Zero Generative AI:** No OpenAI, Gemini, or Claude. Use deterministic NLP (`TextBlob`, `Sumy`).
4.  **Zero Infrastructure Cost:** Run on Vercel Hobby Tier (Serverless).

## Architectural Directives

-   **Frontend:** Next.js (React) + Tailwind CSS. Hosted on Vercel.
-   **Backend:** Python Serverless Functions.
-   **Data Acquisition:** `duckduckgo-search` (time="d" for last 24h).
-   **Content Extraction:** `trafilatura` or `readability-lxml`.
-   **Analysis Engine:**
    -   **Sentiment:** `TextBlob` (Polarity -1 to +1).
    -   **Summarization:** Keyword extraction or LSA.

## Risk Mitigation

-   **Vercel Timeouts:** Use Client-Side Chaining. Frontend parses query and calls API sequentially per ticker.
-   **IP Blocking:** 2-second throttle between requests on the client side.
-   **Library Maintenance:** Pin versions in `requirements.txt`.
