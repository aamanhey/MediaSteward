"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import * as d3 from "d3";

export default function GraphPage() {
  const [graph, setGraph] = useState({ nodes: [], links: [] });

  const loadState = (json) => {
    axios.post("http://localhost:8000/load_state/", json)
      .then(() => {
        // Fetch the updated graph
        axios.get("http://localhost:8000/graph/")
          .then((response) => setGraph(response.data));
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    // Fetch the graph initially
    axios.get("http://localhost:8000/graph/")
      .then((response) => setGraph(response.data))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    // Render the graph with D3
    const svg = d3.select("#graph")
      .attr("width", 800)
      .attr("height", 600);

    svg.selectAll("*").remove(); // Clear previous graph

    const simulation = d3.forceSimulation(graph.nodes)
      .force("link", d3.forceLink(graph.links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(400, 300));

    const link = svg.append("g")
      .selectAll("line")
      .data(graph.links)
      .enter()
      .append("line")
      .style("stroke", "#aaa");

    const node = svg.append("g")
      .selectAll("circle")
      .data(graph.nodes)
      .enter()
      .append("circle")
      .attr("r", 10)
      .style("fill", "blue");

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });
  }, [graph]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const json = JSON.parse(event.target.result);
      loadState(json);
    };
    reader.readAsText(file);
  };

  return (
    <div>
      <h1>Social Network Visualization</h1>
      <input type="file" accept=".json" onChange={handleFileUpload} />
      <svg id="graph"></svg>
    </div>
  );
};