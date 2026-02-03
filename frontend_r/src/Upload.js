import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Upload({ token }) {
  const [file, setFile] = useState(null);
  const [current, setCurrent] = useState(null); // { timestamp, data }
  const [hasUploaded, setHasUploaded] = useState(false);
  const [history, setHistory] = useState([]);

  // Restore history on load
  useEffect(() => {
    const saved = localStorage.getItem("uploadHistory");
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const uploadCSV = async () => {
    if (!file) {
      alert("Pick a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/api/upload/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    const data = await res.json();

    const entry = {
      timestamp: new Date().toLocaleString(),
      data,
    };

    setCurrent(entry);
    setHasUploaded(true);

    const newHistory = [entry, ...history].slice(0, 5);
    setHistory(newHistory);
    localStorage.setItem("uploadHistory", JSON.stringify(newHistory));
  };

  const renderSummary = (data) => (
    <ul>
      {Object.entries(data).map(([key, value]) =>
        typeof value === "number" || typeof value === "string" ? (
          <li key={key}>
            <strong>{key.replaceAll("_", " ")}:</strong> {value}
          </li>
        ) : null
      )}
    </ul>
  );

  const renderChart = (data) =>
    data.equipment_type_distribution ? (
      <Bar
        data={{
          labels: Object.keys(data.equipment_type_distribution),
          datasets: [
            {
              data: Object.values(data.equipment_type_distribution),
              backgroundColor: "#4c72b0",
            },
          ],
        }}
        options={{ plugins: { legend: { display: false } } }}
      />
    ) : null;

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Upload CSV</h3>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />

      <button onClick={uploadCSV}>Upload</button>

      {/* ---------- CURRENT VIEW ---------- */}
      {current && hasUploaded && (
        <>
          <hr />
          <h4>Selected Dataset</h4>
          <small>{current.timestamp}</small>
          {renderSummary(current.data)}
          {renderChart(current.data)}
        </>
      )}

      {/* ---------- HISTORY ---------- */}
      {history.length > 0 && (
        <>
          <hr />
          <h4>Recent Uploads</h4>

          {history.map((item, idx) => (
            <div
              key={idx}
              onClick={() => {
                setCurrent(item);
                setHasUploaded(true);
              }}
              style={{
                cursor: "pointer",
                border: "1px solid #ddd",
                padding: 10,
                marginBottom: 8,
                borderRadius: 4,
                background:
                  current?.timestamp === item.timestamp
                    ? "#f0f4ff"
                    : "#fff",
              }}
            >
              <strong>{item.timestamp}</strong>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default Upload;
