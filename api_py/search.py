from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from textblob import TextBlob
import trafilatura
import os
import re

app = Flask(__name__)


def _summarize(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) >= 2:
        return f"{sentences[0]} {sentences[1]}".strip()
    return sentences[0].strip() if sentences else ""


@app.route("/", methods=["GET"])
def search_and_analyze():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    if os.environ.get("MOCK_SEARCH"):
        return jsonify(
            {
                "results": [
                    {
                        "headline": f"Mock News for {query}",
                        "link": "http://example.com",
                        "snippet": f"{query} sees a massive surge in revenue. Investors are happy.",
                        "sentiment": {"score": 0.5, "label": "Positive"},
                    }
                ]
            }
        )

    results = []
    try:
        ddgs = DDGS()
        search_results = list(ddgs.text(query, max_results=3, timelimit="d"))
        for res in search_results:
            title = res.get("title")
            link = res.get("href")
            snippet = res.get("body", "") or ""

            text = snippet
            try:
                downloaded = trafilatura.fetch_url(link, timeout=8)
                if downloaded:
                    extracted = trafilatura.extract(downloaded)
                    if extracted:
                        text = extracted
            except Exception:
                text = snippet

            sentiment_score = 0.0
            sentiment_label = "Neutral"
            if text:
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
                if sentiment_score > 0.05:
                    sentiment_label = "Positive"
                elif sentiment_score < -0.05:
                    sentiment_label = "Negative"
                snippet = _summarize(text) or snippet

            results.append(
                {
                    "headline": title,
                    "link": link,
                    "snippet": snippet,
                    "sentiment": {
                        "score": sentiment_score,
                        "label": sentiment_label,
                    },
                }
            )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True, port=5328)
