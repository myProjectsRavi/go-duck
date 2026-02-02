import React from 'react';

interface NewsItem {
  headline: string;
  link: string;
  snippet: string;
  sentiment: {
    score: number;
    label: string;
  };
}

const NewsCard = ({ headline, link, snippet, sentiment }: NewsItem) => {
  // Function to highlight keywords
  const getHighlightedText = (text: string) => {
    // Keywords to highlight: Revenue, Crash, Surge
    // Use regex with capturing group to split and keep delimiters
    const parts = text.split(/(Revenue|Crash|Surge)/gi);

    return (
      <span>
        {parts.map((part, i) =>
          ['revenue', 'crash', 'surge'].includes(part.toLowerCase()) ? (
            <span key={i} className="font-bold bg-yellow-200 text-black px-1 rounded-sm mx-0.5 shadow-sm">
              {part}
            </span>
          ) : (
            <span key={i}>{part}</span>
          )
        )}
      </span>
    );
  };

  const badgeColor =
    sentiment.label === 'Positive' ? 'bg-green-100 text-green-700 border-green-200' :
    sentiment.label === 'Negative' ? 'bg-red-100 text-red-700 border-red-200' :
    'bg-gray-100 text-gray-700 border-gray-200';

  return (
    <div className={`flex flex-col p-4 bg-white rounded-xl border shadow-sm hover:shadow-md transition-all duration-200 ${
      sentiment.label === 'Positive' ? 'border-l-4 border-l-green-500' :
      sentiment.label === 'Negative' ? 'border-l-4 border-l-red-500' :
      'border-l-4 border-l-gray-300'
    }`}>
      <div className="flex justify-between items-start gap-3 mb-2">
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className="font-bold text-lg leading-tight text-gray-900 hover:text-blue-600 hover:underline decoration-2 underline-offset-2 transition-colors"
        >
          {headline}
        </a>
        <span className={`text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wider border ${badgeColor}`}>
          {sentiment.label}
        </span>
      </div>

      <p className="text-sm text-gray-600 leading-relaxed mb-3">
        {getHighlightedText(snippet)}
      </p>

      <div className="mt-auto pt-2 border-t border-gray-100 flex justify-between items-center text-xs text-gray-400">
        <span className="truncate max-w-[200px]">{new URL(link).hostname.replace('www.', '')}</span>
        <span>Score: {sentiment.score.toFixed(2)}</span>
      </div>
    </div>
  );
};

export default NewsCard;
