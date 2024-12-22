import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_load_state():
    # Load the initial state
    with open("test_state.json", "r") as f:
        state = json.load(f)

    response = requests.post(f"{BACKEND_URL}/load_state/", json=state)
    assert response.status_code == 200
    print("Load state response:", response.json())

def test_get_graph():
    # Retrieve the graph structure
    response = requests.get(f"{BACKEND_URL}/graph/")
    assert response.status_code == 200
    graph = response.json()
    print("Graph structure:", graph)

if __name__ == "__main__":
    test_load_state()
    test_get_graph()
