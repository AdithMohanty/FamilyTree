import React, { useState } from "react";
import axios from "axios";
import { Network } from "react-vis-network";

function App() {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [path, setPath] = useState(null);
  const [graphData, setGraphData] = useState(null);

  const handleSubmit = async () => {
    if (source && target) {
      try {
        const response = await axios.post("http://localhost:8501/shortest-path", {
          source,
          target,
        });
        setPath(response.data.path);
      } catch (error) {
        console.error("Error finding path", error);
      }
    }
  };

  // Load the graph data
  const loadGraph = async () => {
    try {
      const response = await axios.get("http://localhost:8501/graph-data");
      setGraphData(response.data);
    } catch (error) {
      console.error("Error loading graph", error);
    }
  };

  React.useEffect(() => {
    loadGraph();
  }, []);

  return (
    <div>
      <h1>Family Tree Visualization</h1>
      <div>
        <input
          type="text"
          placeholder="Source Member"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        />
        <input
          type="text"
          placeholder="Target Member"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
        <button onClick={handleSubmit}>Find Shortest Path</button>
      </div>

      {path && (
        <div>
          <h2>Shortest Path:</h2>
          <p>{path.join(" -> ")}</p>
        </div>
      )}

      {graphData && (
        <Network
          data={graphData}
          options={{
            nodes: {
              shape: "dot",
              size: 16,
              font: {
                size: 14,
                color: "#ffffff",
              },
            },
            edges: {
              width: 2,
              color: "#2B7CE9",
            },
          }}
        />
      )}
    </div>
  );
}

export default App;
