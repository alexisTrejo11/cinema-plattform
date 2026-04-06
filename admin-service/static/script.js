const ADMIN_API_URL = 'http://localhost:8000';


async function fetchServices() {
    try {
        const response = await fetch(`${ADMIN_API_URL}/api/v2/admin-manager/available-services`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(data)
        renderServices(data.services);
    } catch(error) {
        console.error("Error fetching services:", error);
        document.getElementById('services-container').innerHTML = '<p style="color: red;">Error while loading services.</p>';
    }
}


function renderServices(services) {
    const container = document.getElementById('services-container');
    container.innerHTML = '';

    if (services.length === 0) {
        container.innerHTML = '<p>No services registred.</p>';
        return;
    }


    services.forEach(service => {
        const card = document.createElement('div');
        card.className = `service-card ${service.status}`;
        card.innerHTML = `
            <h2>${service.service_name}</h2>
            <p><strong>ID de Instancia:</strong> ${service.instance_id}</p>
            <p><strong>Host:</strong> ${service.host}:${service.port}</p>
            <p><strong>Estado:</strong> <span style="font-weight: bold; color: ${service.status === 'UP' ? 'green' : 'red'};">${service.status}</span></p>
            <p><strong>Último Heartbeat:</strong> ${new Date(service.last_heartbeat).toLocaleString()}</p>
        `;
        container.appendChild(card);
    });
}


document.addEventListener('DOMContentLoaded', () => {
    fetchServices();
    setInterval(fetchServices, 5000);
});