document.addEventListener("DOMContentLoaded", function () {
  const svg = document.getElementById("map-svg");
  const container = document.getElementById("map-container");
  const detailPanel = document.getElementById("location-details");
  
  let mapData = { nodes: [], edges: [] };
  let dynamicNodes = [];
  let activeLayers = { bins: true, trucks: true, plants: true };
  let bounds = { minLat: Infinity, maxLat: -Infinity, minLon: Infinity, maxLon: -Infinity };

  // Generate bounds from initial static map data to stop jitter
  async function initMap() {
    try {
      const res = await fetch("/api/map-data");
      mapData = await res.json();
      
      mapData.nodes.forEach(n => {
        bounds.minLat = Math.min(bounds.minLat, n.lat);
        bounds.maxLat = Math.max(bounds.maxLat, n.lat);
        bounds.minLon = Math.min(bounds.minLon, n.lon);
        bounds.maxLon = Math.max(bounds.maxLon, n.lon);
      });
      
      const latP = (bounds.maxLat - bounds.minLat) * 0.15 || 0.01;
      const lonP = (bounds.maxLon - bounds.minLon) * 0.15 || 0.01;
      bounds.minLat -= latP; bounds.maxLat += latP;
      bounds.minLon -= lonP; bounds.maxLon += lonP;

      setInterval(pollDynamcs, 1000);
      pollDynamcs();
    } catch(e) { console.error(e); }
  }

  async function pollDynamcs() {
    try {
      const [binsRes, trucksRes, plantsRes] = await Promise.all([
        fetch('/api/bins-stats'),
        fetch('/api/vehicles-stats'),
        fetch('/api/plants-stats')
      ]);
      const bins = await binsRes.json();
      const trucks = await trucksRes.json();
      const plants = await plantsRes.json();

      // Ensure locations.json is loaded via bins logic if possible, or just use bin coordinates. 
      // Wait, bins output does not have lat/lon directly. Bins are located at location_id.
      // We need location lat/lon. But map-data nodes have lat/lon.
      const locDict = {};
      mapData.nodes.forEach(n => locDict[n.id] = n);

      dynamicNodes = [];
      
      bins.forEach(b => {
        let loc = locDict[b.location_id];
        if(loc) dynamicNodes.push({
          id: b.id, type: 'bin', lat: loc.lat, lon: loc.lon, name: `${loc.name} (${b.current_percentage.toFixed(0)}%)`, area: loc.name, obj: b, emoji: '🗑️'
        });
      });

      trucks.forEach(t => {
        dynamicNodes.push({id: t.id, type: 'truck', lat: t.lat, lon: t.lon, name: t.id, obj: t, emoji: '🚚'});
      });

      plants.segregation.concat(plants.processing).forEach(p => {
        dynamicNodes.push({id: p.id, type: 'plant', lat: p.lat, lon: p.lon, name: p.name, obj: p, emoji: '🏭'});
      });

      render();
    } catch(e) { console.error(e); }
  }

  function render() {
    svg.innerHTML = "";
    const w = container.clientWidth, h = container.clientHeight;
    const sLat = l => h - ((l - bounds.minLat) / (bounds.maxLat - bounds.minLat)) * h;
    const sLon = l => ((l - bounds.minLon) / (bounds.maxLon - bounds.minLon)) * w;

    // Edges
    mapData.edges.forEach(e => {
      const src = mapData.nodes.find(n => n.id === e.source);
      const tgt = mapData.nodes.find(n => n.id === e.target);
      if(src && tgt) {
        let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", sLon(src.lon)); line.setAttribute("y1", sLat(src.lat));
        line.setAttribute("x2", sLon(tgt.lon)); line.setAttribute("y2", sLat(tgt.lat));
        line.setAttribute("stroke", "rgba(255,255,255,0.05)");
        line.setAttribute("stroke-width", "2");
        svg.appendChild(line);
      }
    });

    dynamicNodes.filter(n => activeLayers[n.type + 's']).forEach(n => {
      let g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.style.cursor = 'pointer';
      g.style.transition = 'transform 0.5s ease'; // Smooth movement
      g.setAttribute('transform', `translate(${sLon(n.lon)}, ${sLat(n.lat)})`);
      
      let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.textContent = n.emoji;
      text.setAttribute('font-size', n.type === 'plant' ? '24' : '20');
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('y', '5'); // Vertically center a bit
      g.appendChild(text);

      let label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.textContent = n.name;
      label.setAttribute('y', '25');
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('fill', 'white');
      label.setAttribute('font-size', '10');
      label.setAttribute('paint-order', 'stroke');
      label.setAttribute('stroke', '#111');
      label.setAttribute('stroke-width', '3px');
      g.appendChild(label);

      g.addEventListener('click', () => showDetails(n));
      svg.appendChild(g);
    });
  }

  function showDetails(node) {
      document.getElementById("detail-name").textContent = node.area || node.name;
      document.getElementById("detail-type").textContent = `Type: ${node.type}`;
      let level = 100;
      if (node.type === 'bin') level = node.obj.current_percentage;
      if (node.type === 'truck') level = ((node.obj.capacity - node.obj.available) / node.obj.capacity) * 100;
      if (node.type === 'plant') level = (node.obj.usage / node.obj.capacity) * 100;
      
      document.getElementById("detail-level").textContent = `${level.toFixed(1)}%`;
      document.getElementById("detail-progress").style.width = `${level.toFixed(1)}%`;
      detailPanel.style.display = "block";
  }

  window.toggleLayer = function(layer) {
    if(activeLayers.hasOwnProperty(layer)) { activeLayers[layer] = !activeLayers[layer]; render(); }
  };
  
  initMap();
});
