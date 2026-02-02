import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import trafilatura
from duckduckgo_search import DDGS
from textblob import TextBlob

MAX_RESULTS = 3
MAX_TOTAL_SECONDS = float(os.getenv("SEARCH_MAX_SECONDS", "8.5"))
FETCH_TIMEOUT_SECONDS = float(os.getenv("SEARCH_FETCH_TIMEOUT", "6"))


def _summarize(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) >= 2:
        return f"{sentences[0]} {sentences[1]}".strip()
    return sentences[0].strip() if sentences else ""


def _sentiment_label(score: float) -> str:
    if score > 0.05:
        return "Positive"
    if score < -0.05:
        return "Negative"
    return "Neutral"


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query or "")
        query = (params.get("q") or [""])[0].strip()

        if not query:
            self._send_json(400, {"error": "No query provided"})
            return

        if os.environ.get("MOCK_SEARCH"):
            self._send_json(
                200,
                {
                    "results": [
                        {
                            "headline": f"Mock News for {query}",
                            "link": "http://example.com",
                            "snippet": f"{query} sees a massive surge in revenue. Investors are happy.",
                            "sentiment": {"score": 0.5, "label": "Positive"},
                        }
                    ]
                },
            )
            return

        start = time.monotonic()
        results = []

        try:
            with DDGS() as ddgs:
                search_results = list(
                    ddgs.text(query, max_results=MAX_RESULTS, timelimit="d")
                )

            for res in search_results:
                if time.monotonic() - start > MAX_TOTAL_SECONDS:
                    break

                title = res.get("title") or "Untitled"
                link = res.get("href") or ""
                snippet = res.get("body") or ""

                text = snippet
                remaining = MAX_TOTAL_SECONDS - (time.monotonic() - start)
                if link and remaining > 0.8:
                    try:
                        downloaded = trafilatura.fetch_url(
                            link, timeout=min(FETCH_TIMEOUT_SECONDS, remaining)
                        )
                        if downloaded:
                            extracted = trafilatura.extract(downloaded)
                            if extracted:
                                text = extracted
                    except Exception:
                        text = snippet

                sentiment_score = 0.0
                if text:
                    sentiment_score = TextBlob(text).sentiment.polarity
                    snippet = _summarize(text) or snippet

                results.append(
                    {
                        "headline": title,
                        "link": link,
                        "snippet": snippet,
                        "sentiment": {
                            "score": sentiment_score,
                            "label": _sentiment_label(sentiment_score),
                        },
                    }
                )

            self._send_json(200, {"results": results})
        except Exception as exc:
            self._send_json(500, {"error": str(exc)})

    def log_message(self, format: str, *args) -> None:
        # Reduce noisy logs on serverless runtime.
        return
