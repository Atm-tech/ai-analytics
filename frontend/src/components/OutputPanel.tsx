import React from "react";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

interface Props {
  result: any;
}

export default function OutputPanel({ result }: Props) {
  if (!result) return <p>No results yet.</p>;

  const downloadCSV = () => {
    if (!result.sample_output || !result.sample_output.length) return;

    const ws = XLSX.utils.json_to_sheet(result.sample_output);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Result");
    const buffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    saveAs(new Blob([buffer]), "analysis_result.xlsx");
  };

  return (
    <div>
      <h4>Summary</h4>
      <pre>{result.summary}</pre>

      <h4>Filters Applied</h4>
      {result.filters_applied?.length ? (
        <ul>
          {result.filters_applied.map((f: string, i: number) => (
            <li key={i}>{f}</li>
          ))}
        </ul>
      ) : (
        <p>None</p>
      )}

      <h4>Sample Output</h4>
      {result.sample_output?.length ? (
        <div>
          <table border={1} cellPadding={6}>
            <thead>
              <tr>
                {Object.keys(result.sample_output[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.sample_output.map((row: any, i: number) => (
                <tr key={i}>
                  {Object.values(row).map((val: any, j: number) => (
                    <td key={j}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <button onClick={downloadCSV} style={{ marginTop: 10, padding: "6px 12px" }}>
            Download as Excel
          </button>
        </div>
      ) : (
        <p>No data available.</p>
      )}
    </div>
  );
}
