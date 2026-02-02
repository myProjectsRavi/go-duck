from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from textblob import TextBlob
import trafilatura
import os

app = Flask(__name__)

# To prevent CORS issues during local dev if needed, or Vercel handles it?
# Usually in Next.js rewrites, it's fine. But for direct access, let's keep it simple.

@app.route('/api/search', methods=['GET'])
def search_and_analyze():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    results = []
    try:
        # Mock search for testing to avoid rate limits if env var set
        if os.environ.get('MOCK_SEARCH'):
            results = [
                {
                    'headline': f"Mock News for {query}",
                    'link': "http://example.com",
                    'snippet': f"{query} sees a massive surge in revenue. Investors are happy.",
                    'sentiment': {'score': 0.5, 'label': 'Positive'}
                }
            ]
            return jsonify({'results': results})

        ddgs = DDGS()
        # Search for news - specifically use news? ddgs.news() or ddgs.text()?
        # Requirements said: "search DuckDuckGo for a specific keyword, fetch the top 3 results"
        # and "timelimit='d'". ddgs.text() supports timelimit. ddgs.news() also does.
        # ddgs.text() is broader. Let's use ddgs.text() as requested.
        search_results = list(ddgs.text(query, max_results=3, timelimit='d'))

        for res in search_results:
            title = res.get('title')
            link = res.get('href')
            snippet = res.get('body', '') # Fallback snippet

            # Extract content using trafilatura
            try:
                downloaded = trafilatura.fetch_url(link)
                if downloaded:
                    text = trafilatura.extract(downloaded)
                else:
                    text = snippet
            except:
                text = snippet

            sentiment_score = 0
            sentiment_label = "Neutral"

            if text:
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
                if sentiment_score > 0.05:
                    sentiment_label = "Positive"
                elif sentiment_score < -0.05:
                    sentiment_label = "Negative"

                # Update snippet to be first 2 sentences if text is available
                # robust enough sentence splitting without NLTK
                import re
                sentences = re.split(r'(?<=[.!?])\s+', text)
                if len(sentences) >= 2:
                    snippet = sentences[0] + " " + sentences[1]
                elif len(sentences) > 0:
                    snippet = sentences[0]

            results.append({
                'headline': title,
                'link': link,
                'snippet': snippet,
                'sentiment': {
                    'score': sentiment_score,
                    'label': sentiment_label
                }
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5328)
