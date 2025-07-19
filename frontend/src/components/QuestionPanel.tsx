import React from "react";
import axios from "axios";

interface Props {
  question: string;
  setQuestion: (q: string) => void;
  definitions: string[];
  setResult: (r: any) => void;
}

export default function QuestionPanel({ question, setQuestion, definitions, setResult }: Props) {
  const ask = async () => {
    if (!question.trim()) return;

    try {
      const res = await axios.post("http://localhost:8000/api/query/analyze", {
        question,
        definitions,
      });

      setResult(res.data);
    } catch (err) {
      alert("Query failed. Check console.");
      console.error(err);
    }
  };

  return (
    <div>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="e.g. What are the superfast products?"
        rows={3}
        style={{ width: "100%", padding: 8 }}
      />

      <button onClick={ask} style={{ marginTop: 10, padding: "6px 12px" }}>
        Analyze
      </button>
    </div>
  );
}
``
