document.addEventListener("DOMContentLoaded", function () {
  const svg = document.getElementById("map-svg");
  const container = document.getElementById("map-container");

  // Fetch map data
  fetch("/api/map-data")
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error:", data.error);
        return;
      }

      drawMap(data.nodes, data.edges);
    })
    .catch((error) => {
      console.error("Error fetching map data:", error);
    });

  function drawMap(nodes, edges) {
    // Clear previous content
    svg.innerHTML = "";

    if (nodes.length === 0) {
      svg.innerHTML =
        '<text x="50%" y="50%" text-anchor="middle" font-size="20">No map data available</text>';
      return;
    }

    // Calculate bounds
    let minLat = Infinity,
      maxLat = -Infinity,
      minLon = Infinity,
      maxLon = -Infinity;
    nodes.forEach((node) => {
      minLat = Math.min(minLat, node.lat);
      maxLat = Math.max(maxLat, node.lat);
      minLon = Math.min(minLon, node.lon);
      maxLon = Math.max(maxLon, node.lon);
    });

    // Add some padding
    const latRange = maxLat - minLat || 1;
    const lonRange = maxLon - minLon || 1;
    const padding = 0.01;
    minLat -= latRange * padding;
    maxLat += latRange * padding;
    minLon -= lonRange * padding;
    maxLon += lonRange * padding;

    // Scale to SVG dimensions
    const width = container.clientWidth;
    const height = container.clientHeight;

    function scaleLat(lat) {
      return height - ((lat - minLat) / (maxLat - minLat)) * height;
    }

    function scaleLon(lon) {
      return ((lon - minLon) / (maxLon - minLon)) * width;
    }

    // Draw edges
    edges.forEach((edge) => {
      const sourceNode = nodes.find((n) => n.id === edge.source);
      const targetNode = nodes.find((n) => n.id === edge.target);

      if (sourceNode && targetNode) {
        const line = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "line",
        );
        line.setAttribute("x1", scaleLon(sourceNode.lon));
        line.setAttribute("y1", scaleLat(sourceNode.lat));
        line.setAttribute("x2", scaleLon(targetNode.lon));
        line.setAttribute("y2", scaleLat(targetNode.lat));
        line.classList.add("edge");
        svg.appendChild(line);
      }
    });

    // Draw nodes
    nodes.forEach((node) => {
      const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle",
      );
      circle.setAttribute("cx", scaleLon(node.lon));
      circle.setAttribute("cy", scaleLat(node.lat));
      circle.setAttribute("r", 5);
      circle.classList.add("node");
      circle.classList.add(node.type);
      circle.setAttribute("title", `${node.name} (${node.type})`);
      svg.appendChild(circle);

      // Add label
      const text = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text",
      );
      text.setAttribute("x", scaleLon(node.lon));
      text.setAttribute("y", scaleLat(node.lat) - 8);
      text.classList.add("node-label");
      text.textContent = node.name.split(" ")[0]; // First word only
      svg.appendChild(text);
    });
  }
});
