from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
import json

app = FastAPI()
graph = nx.Graph()

class Node(BaseModel):
    id: str
    label: str

class Edge(BaseModel):
    source: str
    target: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello World!"}

@app.post("/add_node/")
def add_node(node: Node):
    graph.add_node(node.id, label=node.label)
    return {"message": f"Node {node.label} added."}

@app.post("/add_edge/")
def add_edge(edge: Edge):
    graph.add_edge(edge.source, edge.target)
    return {"message": f"Edge from {edge.source} to {edge.target} added."}

@app.get("/graph/")
def get_graph():
    return nx.node_link_data(graph)

@app.post("/load_state/")
def load_state(state: dict):
    # Clear the graph and load the new state
    graph.clear()
    for node in state.get("nodes", []):
        graph.add_node(node["id"], label=node["label"])
    for edge in state.get("links", []):
        graph.add_edge(edge["source"], edge["target"])
    return {"message": "Graph state loaded successfully."}
