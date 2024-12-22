let graph = { nodes: [], links: [] }; // In-memory graph

export default function handler(req, res) {
  if (req.method === "GET") {
    res.status(200).json(graph); // Return graph
  } else if (req.method === "POST") {
    const { nodes, links } = req.body;
    graph = { nodes, links }; // Update graph
    res.status(200).json({ message: "Graph updated" });
  } else {
    res.setHeader("Allow", ["GET", "POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
