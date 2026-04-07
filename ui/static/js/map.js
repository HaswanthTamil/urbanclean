document.addEventListener("DOMContentLoaded", function () {
  const svg = document.getElementById("map-svg");
  const container = document.getElementById("map-container");
  const detailPanel = document.getElementById("location-details");
  
  let mapData = { nodes: [], edges: [] };
  let activeLayers = { bins: true, trucks: true, plants: true };

  // Fetch map data
  async function fetchMapData() {
    try {
      const response = await fetch("/api/map-data");
      const data = await response.json();
      if (data.error) {
        console.error("Error:", data.error);
        return;
      }
      mapData = data;
      render();
    } catch (error) {
      console.error("Error fetching map data:", error);
    }
  }

  function render() {
    // Filter nodes based on active layers
    const filteredNodes = mapData.nodes.filter(node => {
        if (node.type === 'collection_point') return activeLayers.bins;
        if (node.type === 'truck') return activeLayers.trucks;
        if (node.type.includes('plant')) return activeLayers.plants;
        return true;
    });

    // Only draw edges between nodes that are both visible
    const visibleNodeIds = new Set(filteredNodes.map(n => n.id));
    const filteredEdges = mapData.edges.filter(edge => 
        visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target)
    );

    drawMap(filteredNodes, filteredEdges);
  }

  function drawMap(nodes, edges) {
    // Clear previous content
    svg.innerHTML = "";

    if (nodes.length === 0 && mapData.nodes.length > 0) {
      svg.innerHTML =
        '<text x="50%" y="50%" text-anchor="middle" font-size="20" fill="white">All layers hidden. Toggle filters to view map assets.</text>';
      return;
    } else if (nodes.length === 0) {
        svg.innerHTML =
        '<text x="50%" y="50%" text-anchor="middle" font-size="20" fill="white">Connecting to server...</text>';
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
    const latRange = maxLat - minLat || 0.01;
    const lonRange = maxLon - minLon || 0.01;
    const padding = 0.15; // Increased padding for better view
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
        line.setAttribute("stroke", "rgba(15, 23, 42, 0.15)");
        line.setAttribute("stroke-width", "1.5");
        svg.appendChild(line);
      }
    });

    // Draw nodes
    nodes.forEach((node) => {
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.classList.add("node-group");
      
      const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle",
      );
      circle.setAttribute("cx", scaleLon(node.lon));
      circle.setAttribute("cy", scaleLat(node.lat));
      circle.setAttribute("r", node.type.includes('plant') ? 8 : 5);
      circle.classList.add("node");
      circle.classList.add(node.type);
      circle.setAttribute("id", `node-${node.id}`);
      
      // Node tooltips/click behavior
      circle.addEventListener('click', () => {
          showDetails(node);
      });

      g.appendChild(circle);

      // Add label
      const text = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text",
      );
      text.setAttribute("x", scaleLon(node.lon));
      text.setAttribute("y", scaleLat(node.lat) - (node.type.includes('plant') ? 12 : 10));
      text.classList.add("node-label");
      text.setAttribute("text-anchor", "middle");
      text.textContent = node.name;
      g.appendChild(text);
      
      svg.appendChild(g);
    });
  }

  function showDetails(node) {
      document.getElementById("detail-name").textContent = node.name;
      document.getElementById("detail-type").textContent = `Type: ${node.type.replace('_', ' ')}`;
      
      // Mock progress for demo purposes
      const level = Math.floor(Math.random() * 100);
      document.getElementById("detail-level").textContent = `${level}%`;
      document.getElementById("detail-progress").style.width = `${level}%`;
      
      detailPanel.style.display = "block";
  }

  // Define toggleLayer globally
  window.toggleLayer = function(layer) {
    if (activeLayers.hasOwnProperty(layer)) {
      activeLayers[layer] = !activeLayers[layer];
      render();
    }
  };

  // Initial fetch
  fetchMapData();
  
  // Resize handler
  window.addEventListener('resize', () => {
      if (mapData.nodes.length > 0) render();
  });
});
