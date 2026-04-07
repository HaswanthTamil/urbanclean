/* Dashboard Logic for Urban Clean */

async function fetchStats() {
    try {
        const [binsRes, trucksRes, plantsRes] = await Promise.all([
            fetch('/api/bins-stats'),
            fetch('/api/vehicles-stats'),
            fetch('/api/plants-stats')
        ]);

        const bins = await binsRes.json();
        const trucks = await trucksRes.json();
        const plants = await plantsRes.json();

        updateOverviewStats(bins, trucks, plants);
        updatePriorityList(bins);
        updateFleetTable(trucks);
        updatePlantsTable(plants);
    } catch (error) {
        console.error("Error fetching stats:", error);
    }
}

function updateOverviewStats(bins, trucks, plants) {
    document.getElementById("stat-bins").textContent = bins.length;
    document.getElementById("stat-trucks").textContent = trucks.filter(t => t.status === 'active').length;
    
    // Total waste processed (mock sum)
    const totalProcessed = plants.processing.reduce((acc, p) => acc + p.usage, 0) / 1000;
    document.getElementById("stat-waste").innerHTML = totalProcessed.toFixed(1) + ' <span style="font-size: 1rem;">tons</span>';
    
    // Alerts: bins with high fill level
    const criticalBins = bins.filter(b => b.current_percentage > 85).length;
    document.getElementById("stat-alerts").textContent = criticalBins;
}

function updatePriorityList(bins) {
    const list = document.getElementById("priority-list");
    if (!list) return;
    
    const priorityBins = bins
        .filter(b => b.current_percentage > 70)
        .sort((a, b) => b.current_percentage - a.current_percentage)
        .slice(0, 5);

    list.innerHTML = priorityBins.map(bin => `
        <div style="padding: 1rem; background: var(--glass-bg); border-radius: 0.75rem; margin-bottom: 0.75rem; border-left: 4px solid ${bin.current_percentage > 85 ? 'var(--danger)' : 'var(--accent)'};">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="font-weight: 600; font-size: 0.875rem;">${bin.id}</span>
                <span style="color: ${bin.current_percentage > 85 ? 'var(--danger)' : 'var(--accent)'}; font-size: 0.75rem; font-weight: 700;">${bin.current_percentage > 85 ? 'CRITICAL' : 'HIGH'}</span>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Fill Level: ${Math.round(bin.current_percentage)}% • Type: ${bin.waste_type.join(', ')}</div>
        </div>
    `).join('');
}

function updateFleetTable(trucks) {
    const container = document.getElementById("fleet-status");
    if (!container) return;
    
    container.innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
            <thead>
                <tr style="text-align: left; color: var(--text-muted); border-bottom: 1px solid var(--border);">
                    <th style="padding: 1rem 0;">ID</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Capacity</th>
                </tr>
            </thead>
            <tbody>
                ${trucks.map(t => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 1rem 0;">${t.id}</td>
                        <td>${t.type}</td>
                        <td><span class="dot ${t.status === 'active' ? 'dot-green' : 'dot-amber'}"></span> ${t.status}</td>
                        <td>${Math.round((1 - t.available/t.capacity) * 100)}%</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function updatePlantsTable(plants) {
    const container = document.getElementById("plants-status");
    if (!container) return;

    const allPlants = [...plants.segregation.map(p => ({...p, type: 'Segregation'})), ...plants.processing.map(p => ({...p, type: 'Processing'}))];
    
    container.innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
            <thead>
                <tr style="text-align: left; color: var(--text-muted); border-bottom: 1px solid var(--border);">
                    <th style="padding: 1rem 0;">Plant ID</th>
                    <th>Type</th>
                    <th>Usage</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                ${allPlants.map(p => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 1rem 0;">${p.id}</td>
                        <td>${p.type}</td>
                        <td>${Math.round((p.usage/p.capacity) * 100)}%</td>
                        <td><span class="dot ${p.status === 'working' ? 'dot-green' : 'dot-red'}"></span> ${p.status}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function simulateCheckup() {
    addLog("Initiating manual bin checkup protocol...");
    setTimeout(() => {
        addLog("Sensors recalibrated. Data synchronized.");
    }, 1500);
}

function rerouteTrucks() {
    addLog("Rerouting fleet to optimize high-priority zones.");
    fetchStats();
}

function raisePenalty() {
    const plantId = "PLANT-" + Math.floor(Math.random() * 9000 + 1000);
    addLog(`WARNING: Environmental violation detected at ${plantId}. Penalty issued: ₹25,000.`);
}

function addLog(msg) {
    const logs = document.getElementById("logs");
    if (logs) {
        const time = new Date().toLocaleTimeString([], { hour12: false });
        logs.innerHTML = `[${time}] ${msg}<br>${logs.innerHTML}`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetchStats();
    setInterval(fetchStats, 5000);
    addLog("Command Center initialized. All modules loaded.");
});
