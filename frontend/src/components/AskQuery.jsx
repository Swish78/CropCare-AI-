import React, { useState } from 'react';
import axios from 'axios';

function AskQuery() {
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState('');
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleAsk = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('http://127.0.0.1:5000/ask_pdf', { query });
            setAnswer(response.data.answer);
            setSources(response.data.sources);
        } catch (error) {
            console.error('Error asking the query:', error);
            setError('Error asking the query');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div id="ask-query" className="container mx-auto p-4">
            <h2 className="text-2xl mb-4" style={{ color: '#597445' }}>Ask Query</h2>
            <div className="p-4 border rounded shadow-lg" style={{ backgroundColor: '#E7F0DC' }}>
                <textarea
                    value={query}
                    onChange={handleQueryChange}
                    className="w-full p-2 mb-4 border rounded"
                    placeholder="Enter your query"
                />
                <button
                    onClick={handleAsk}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                    disabled={loading}
                >
                    {loading ? <span className="animate-spin">🔄</span> : 'Ask'}
                </button>
                {error && (
                    <div className="mt-4 text-red-500">
                        <p>{error}</p>
                    </div>
                )}
                {answer && (
                    <div className="mt-4">
                        <h3 className="text-xl" style={{ color: '#658147' }}>Answer</h3>
                        <p>{answer}</p>
                    </div>
                )}
                {sources.length > 0 && (
                    <div className="mt-4">
                        <h3 className="text-xl" style={{ color: '#658147' }}>Sources</h3>
                        <ul>
                            {sources.map((source, index) => (
                                <li key={index} className="mb-2">
                                    <strong>Source:</strong> {source.source}
                                    <p>{source.page_content}</p>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AskQuery;
