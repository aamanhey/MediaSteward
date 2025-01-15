"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import * as d3 from "d3";
import styles from "../page.module.css";

export default function HomePage() {
  const [graph, setGraph] = useState({ nodes: [], links: [] });

  const loadState = (json) => {
    axios.post("http://localhost:8000/load_state/", json)
      .then(() => {
        // Fetch the updated graph
        axios.get("http://localhost:8000/graph/")
          .then((response) => setGraph(response.data))
          .catch((err) => console.error(err));
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    // Trigger loadState when the component mounts
    const initialState = {
      nodes: [
        {"id": "1", "label": "Group A", "lat": 51.505, "lng": -0.09},
        {"id": "2", "label": "Group B", "lat": 51.515, "lng": -0.1},
        {"id": "3", "label": "Group C", "lat": 51.525, "lng": -0.11},
        {"id": "4", "label": "Group D", "lat": 51.535, "lng": -0.12},
        {"id": "5", "label": "Group E", "lat": 51.545, "lng": -0.13},
        {"id": "6", "label": "Group F", "lat": 51.555, "lng": -0.14},
        {"id": "7", "label": "Group G", "lat": 51.565, "lng": -0.15},
        {"id": "8", "label": "Group H", "lat": 51.575, "lng": -0.16},
        {"id": "9", "label": "Group I", "lat": 51.585, "lng": -0.17},
        {"id": "10", "label": "Group J", "lat": 51.595, "lng": -0.18}
      ],
      links: [
        {"source": "1", "target": "2"},
        {"source": "2", "target": "3"},
        {"source": "3", "target": "4"},
        {"source": "4", "target": "5"},
        {"source": "5", "target": "6"},
        {"source": "6", "target": "7"},
        {"source": "7", "target": "8"},
        {"source": "8", "target": "9"},
        {"source": "9", "target": "10"},
        {"source": "10", "target": "1"},
        {"source": "1", "target": "5"},
        {"source": "2", "target": "6"},
        {"source": "3", "target": "7"},
        {"source": "4", "target": "8"},
        {"source": "5", "target": "9"}
      ]
    };
    loadState(initialState);
  }, []);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const json = JSON.parse(e.target.result);
      loadState(json);
    };
    reader.readAsText(file);
  };

  useEffect(() => {
    // Animate nodes between positions
    const svg = d3.select("#graph-overlay")
      .attr("width", 800)
      .attr("height", 600);

    const link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link")
      .style("stroke", "#aaa");

    const node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", "#69b3a2");

    const simulation = d3.forceSimulation(graph.nodes)
      .force("link", d3.forceLink(graph.links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(400, 300))
      .on("tick", () => {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
      });

    return () => simulation.stop();
  }, [graph]);

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Graph Overlay</h1>
        <input type="file" accept=".json" onChange={handleFileUpload} />
        <svg id="graph-overlay" style={{ width: "100%", height: "600px" }}></svg>
      </main>
      <footer className={styles.footer}></footer>
    </div>
  );
}