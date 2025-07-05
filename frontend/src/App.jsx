import axios from "axios";
import { useState } from "react";
import "./index.css";

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [timestamp, setTimestamp] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/analyze", { topic });
      setData(res.data);
      setTimestamp(Date.now()); // used to force image refresh
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Wikipedia Sentiment Analyzer</h1>
        <form onSubmit={handleSubmit} className="flex gap-4 mb-6">
          <input
            type="text"
            placeholder="Enter Wikipedia topic"
            className="p-2 rounded border flex-1"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Analyze
          </button>
        </form>

        {loading && <p>Loading...</p>}

        {data && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">📊 Summary</h2>
            <p><strong>Polarity:</strong> {data.polarity}</p>
            <p><strong>Word Count:</strong> {data.word_count}</p>

            <div>
              <h3 className="font-bold">🟢 Positive Sentences</h3>
              {data.positive_sentences.map((s, i) => (
                <p key={i} className="text-green-700">✔ {s}</p>
              ))}
            </div>

            <div>
              <h3 className="font-bold">🔴 Negative Sentences</h3>
              {data.negative_sentences.map((s, i) => (
                <p key={i} className="text-red-700">✖ {s}</p>
              ))}
            </div>

            <div>
              <h3 className="font-bold">🟡 Neutral Sentences</h3>
              {data.neutral_sentences.map((s, i) => (
                <p key={i} className="text-yellow-700">- {s}</p>
              ))}
            </div>

            <div>
              <h3 className="font-bold">📈 Visuals</h3>
              <img
                src={`http://localhost:5000/static/wordcloud.png?${timestamp}`}
                alt="Word Cloud"
                className="rounded"
              />
              <img
                src={`http://localhost:5000/static/bar_chart.png?${timestamp}`}
                alt="Bar Chart"
                className="rounded mt-4"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
