"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<"idle" | "searching" | "analyzing">("idle");
  const [submittedQuery, setSubmittedQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setSubmittedQuery(query);
    setStatus("searching");

    // Mock transition to analyzing
    setTimeout(() => {
      setStatus("analyzing");
    }, 2000); // 2 seconds delay
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24 bg-gray-50 dark:bg-zinc-900">
      <div className="w-full max-w-2xl flex flex-col items-center">

        {/* Status Indicators */}
        <div className="mb-8 min-h-[3rem] flex items-center justify-center">
            {status === "searching" && (
              <div className="text-xl font-medium animate-pulse text-blue-600 dark:text-blue-400">
                Searching for [{submittedQuery}]...
              </div>
            )}
            {status === "analyzing" && (
              <div className="text-xl font-medium animate-pulse text-purple-600 dark:text-purple-400">
                Analyzing Sentiment...
              </div>
            )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="w-full relative group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask Zero-Scout..."
            className="w-full p-4 pr-16 text-lg bg-white dark:bg-zinc-800 border border-gray-200 dark:border-zinc-700 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all dark:text-white"
            disabled={status !== "idle"}
            autoFocus
          />
          <button
            type="submit"
            disabled={status !== "idle" || !query.trim()}
            className="absolute right-2 top-2 bottom-2 px-4 rounded-xl bg-black text-white dark:bg-white dark:text-black font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:opacity-80 transition-opacity"
          >
            →
          </button>
        </form>

      </div>
    </main>
  );
}
