'use client';

import { useState, useRef, useEffect } from 'react';
import NewsCard from '@/components/NewsCard';

interface NewsItem {
  headline: string;
  link: string;
  snippet: string;
  sentiment: {
    score: number;
    label: string;
  };
}

interface SearchResult {
  ticker: string;
  news: NewsItem[];
  status: 'pending' | 'loading' | 'complete' | 'error';
  error?: string;
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const resultsEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    resultsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [results]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isProcessing) return;

    setIsProcessing(true);

    // Parse query: split by commas or "and"
    // Requirement says "Google, Tesla" or "Google and Tesla"
    const tickers = query.split(/,| and /i).map(t => t.trim()).filter(t => t.length > 0);

    // Initial state for all tickers
    // If results already exist, we append? Or clear?
    // Chat interface usually appends. But here "Fire and Forget" implies new query.
    // Let's replace for simplicity or append to history.
    // The prompt says "input my portfolio tickers... system instantly scrapes... presents highlight summary".
    // I'll replace for now to keep it clean, or append if user wants history.
    // "Chat UI" implies history.
    // I'll append to existing results if any?
    // Actually, let's start fresh for each submission to avoid clutter, or append.
    // Let's clear for now as it's a "Fire and Forget" tool.

    const newResults: SearchResult[] = tickers.map(t => ({
      ticker: t,
      news: [],
      status: 'pending'
    }));
    setResults(newResults);

    // Process sequentially with throttle
    for (let i = 0; i < tickers.length; i++) {
      const ticker = tickers[i];

      // Update status to loading
      setResults(prev => prev.map((item, idx) =>
        item.ticker === ticker && item.status === 'pending' ? { ...item, status: 'loading' } : item
      ));

      try {
        // Use ticker + " stock news" or just ticker? Prompt says "Check latest news for Google".
        // If user enters "Google", we search "Google".
        // Maybe append "news" to query? "Google news".
        // The prompt says "types a natural language query... e.g. Check latest news for Google and Tesla".
        // So I should parse the query better?
        // "Fronted must parse the query (e.g. 'Google, Tesla')..."
        // If user types "Check latest news for Google and Tesla", my split logic will be messy.
        // It's "Zero Generative AI", so I can't use LLM to extract entities.
        // I have to assume user types comma separated list or use regex.
        // But user story says "types a natural language query".
        // If I use TextBlob on frontend? No, frontend is React.
        // I will assume simple input "Google, Tesla" for MVP as per "Epic 1" detail: "parse the query (e.g. 'Google, Tesla')".
        // I'll strip common stop words "Check latest news for" if I want to be fancy, but let's stick to simple splitting.

        const response = await fetch(`/api/search?q=${encodeURIComponent(ticker + " news")}`);
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();

        // Update with data
        setResults(prev => prev.map((item, idx) =>
          item.ticker === ticker && item.status === 'loading' ? { ...item, status: 'complete', news: data.results || [] } : item
        ));
      } catch (err) {
        setResults(prev => prev.map((item, idx) =>
          item.ticker === ticker && item.status === 'loading' ? { ...item, status: 'error', error: 'Failed to fetch news' } : item
        ));
      }

      // Throttle if not last
      if (i < tickers.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }

    setIsProcessing(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 text-gray-900 font-sans">
      <div className="w-full max-w-2xl flex flex-col gap-4 h-[85vh] overflow-y-auto mb-20 p-4 scrollbar-hide">
        {results.length === 0 && !isProcessing && (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <h1 className="text-4xl font-bold mb-4 tracking-tight">Zero-Scout</h1>
            <p className="max-w-md">Enter your portfolio tickers (e.g., "Google, Tesla") to get the latest market intelligence.</p>
          </div>
        )}

        {results.map((res, idx) => (
          <div key={idx} className="flex flex-col gap-3 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-3 border-b pb-2 border-gray-200">
              <div className={`w-3 h-3 rounded-full ${
                res.status === 'loading' ? 'bg-blue-500 animate-pulse' :
                res.status === 'complete' ? 'bg-green-500' :
                res.status === 'error' ? 'bg-red-500' : 'bg-gray-300'
              }`} />
              <h2 className="font-bold text-xl capitalize">{res.ticker}</h2>
              {res.status === 'loading' && <span className="text-sm text-gray-400 italic">Scanning open web...</span>}
            </div>

            {res.status === 'error' && <div className="text-red-500 text-sm p-2 bg-red-50 rounded">Error fetching data.</div>}

            {res.status === 'complete' && (
              <div className="grid grid-cols-1 gap-4">
                {res.news.length === 0 ? (
                  <p className="text-sm text-gray-500 italic">No significant news found in the last 24 hours.</p>
                ) : (
                  res.news.map((item, nIdx) => (
                    <NewsCard key={nIdx} {...item} />
                  ))
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={resultsEndRef} />
      </div>

      <div className="fixed bottom-0 w-full max-w-2xl bg-white p-4 border-t border-gray-200 shadow-lg z-10">
        <form onSubmit={handleSubmit} className="flex gap-2 relative">
          <input
            type="text"
            className="flex-1 p-3 pl-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-shadow"
            placeholder="Search tickers (e.g. Google, Tesla)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isProcessing}
          />
          <button
            type="submit"
            className="bg-black text-white px-6 py-2 rounded-full font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors disabled:cursor-not-allowed"
            disabled={isProcessing || !query.trim()}
          >
            {isProcessing ? '...' : 'Scout'}
          </button>
        </form>
      </div>
    </main>
  );
}
