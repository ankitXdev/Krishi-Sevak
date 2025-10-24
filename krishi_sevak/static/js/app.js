// Initialize theme and load default section
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Show dashboard by default
    showSection('dashboard');
    quickStatus();
    loadMandiPrices();

    // Load default city weather (Agra)
    loadWeatherData('Agra');
});


// Theme toggle: light/dark mode
document.getElementById('themeToggle').addEventListener('click', () => {
    const el = document.body;
    const currentTheme = el.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    el.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

// Update theme icon (🌙 or ☀️)
function updateThemeIcon(theme) {
    document.getElementById('themeToggle').innerText = theme === 'dark' ? '☀️' : '🌙';
}


// Navigation: Show selected section
function showSection(key) {
    // Hide all sections
    document.querySelectorAll('[id^="section-"]').forEach(section => {
        section.style.display = 'none';
    });

    // Remove active class from all nav links
    document.querySelectorAll('.sidebar nav a').forEach(a => {
        a.classList.remove('active');
    });

    // Activate selected link and section
    document.getElementById(`nav-${key}`).classList.add('active');
    document.getElementById(`section-${key}`).style.display = 'block';

    // If weather tab is opened, reload with current city
    if (key === 'weather') {
        const city = document.getElementById('city-select')?.value || 'Agra';
        loadWeatherData(city);
    }
}


// Quick status: Check backend component health
async function quickStatus() {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        const text = `Components: ${data.models.huggingface_model ? '✓' : '✗'} Disease AI ${data.models.crop_recommendation_model ? '✓' : '✗'} Crop Model`;
        document.getElementById('quick-status').innerText = text;
    } catch (e) {
        document.getElementById('quick-status').innerText = 'Unable to connect';
    }
}


// Crop Recommendation Form
document.getElementById('recommend-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    const resultDiv = document.getElementById('recommend-result');
    resultDiv.innerHTML = '<div class="spinner"></div> Processing...';

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        resultDiv.innerHTML = `
            <h4>Recommended Crop: ${result.crop.toUpperCase()}</h4>
            <p>Best grown in ${result.details.best_state} during ${result.details.season} season.</p>
            <p>Water requirement: ${result.details.water}, Temperature: ${result.details.temperature}</p>
            <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
        `;
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: var(--error)">Error: Could not get recommendation</p>`;
    }
});


// Disease Detection: Preview uploaded image
document.getElementById('disease-image').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image-preview').innerHTML = `<img src="${e.target.result}" alt="Leaf image" style="max-width:100%; border-radius:8px;">`;
        };
        reader.readAsDataURL(file);
    }
});

// Analyze image for disease
async function detectDisease() {
    const resultDiv = document.getElementById('detect-result');
    resultDiv.innerHTML = '<div class="spinner"></div> Analyzing image...';

    setTimeout(async () => {
        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const result = await response.json();
            resultDiv.innerHTML = `
                <h4>Disease Detected: ${result.disease}</h4>
                <p>Severity: <strong>${result.severity}</strong></p>
                <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                <p><strong>Solution:</strong> ${result.solution}</p>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<p style="color: var(--error)">Error: Could not analyze image</p>`;
        }
    }, 1500);
}


// Weather Data: Load for selected city
async function loadWeatherData(city = 'Agra') {
    try {
        // Update UI immediately
        document.getElementById('weather-city').textContent = city;

        // Fetch weather data with city parameter
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();

        // Update current weather
        document.getElementById('weather-temp').textContent = `${data.temperature}°C`;
        document.getElementById('weather-condition').textContent = data.condition;

        // Update 7-day forecast
        const forecastContainer = document.getElementById('forecast-container');
        forecastContainer.innerHTML = '';

        data.forecast.forEach(day => {
            const item = document.createElement('div');
            item.className = 'forecast-item';
            item.innerHTML = `
                <div><strong>${day.day}</strong></div>
                <div>${day.temp}°C</div>
                <div>${day.condition}</div>
            `;
            forecastContainer.appendChild(item);
        });

    } catch (error) {
        console.error('Weather fetch failed:', error);
        document.getElementById('weather-data').innerHTML = `
            <p style="color: var(--error)">❌ Could not load weather for ${city}</p>`;
    }
}


// Mandi Prices
async function loadMandiPrices() {
    try {
        const response = await fetch('/api/mandi');
        const data = await response.json();

        // Update location info with cities count and source
        document.getElementById('mandi-location').textContent = 
            data.location || 'Mandi Prices';

        const tbody = document.getElementById('mandi-prices');
        tbody.innerHTML = '';

        if (data.commodities && data.commodities.length > 0) {
            data.commodities.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.name || 'Unknown'}</td>
                    <td>${item.city || 'N/A'}</td>
                    <td><strong>₹${item.price || 'N/A'}</strong></td>
                    <td>${item.unit || 'per quintal'}</td>
                    <td class="muted">${item.variety || 'Common'}</td>
                `;
                tbody.appendChild(row);
            });
        } else {
            // Fallback if no commodities received
            tbody.innerHTML = '<tr><td colspan="5">No price data available</td></tr>';
        }
    } catch (error) {
        console.error('Error loading mandi prices:', error);
        document.getElementById('mandi-prices').innerHTML = 
            '<tr><td colspan="5">Could not load prices</td></tr>';
    }
}



// Crop Information (static data)
function showCropInfo() {
    const select = document.getElementById('crop-select');
    const resultDiv = document.getElementById('crop-info');
    const crop = select.value;

    if (!crop) {
        resultDiv.innerHTML = '<p>Please select a crop to see information</p>';
        return;
    }

    const cropData = {
        wheat: {
            name: 'Wheat', season: 'Rabi', water: '450-600 mm', temp: '10-15°C',
            states: 'Punjab, Haryana, Uttar Pradesh',
            tips: 'Sow from October to December. Apply nitrogen fertilizer in splits.'
        },
        rice: {
            name: 'Rice', season: 'Kharif', water: '1000-1500 mm', temp: '20-35°C',
            states: 'West Bengal, Uttar Pradesh, Andhra Pradesh',
            tips: 'Requires flooded fields. Use System of Rice Intensification (SRI) for better yields.'
        },
        corn: {
            name: 'Corn', season: 'Kharif', water: '500-700 mm', temp: '20-27°C',
            states: 'Karnataka, Andhra Pradesh, Tamil Nadu',
            tips: 'Plant in rows with 60cm spacing. Control stem borers with neem-based pesticides.'
        }
    };

    const data = cropData[crop];
    resultDiv.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
            <div class="card">
                <strong>Season</strong>
                <div>${data.season}</div>
            </div>
            <div class="card">
                <strong>Water Requirement</strong>
                <div>${data.water}</div>
            </div>
            <div class="card">
                <strong>Temperature</strong>
                <div>${data.temp}</div>
            </div>
            <div class="card">
                <strong>Best States</strong>
                <div>${data.states}</div>
            </div>
        </div>
        <div style="margin-top: 16px;">
            <strong>Farming Tips:</strong>
            <p>${data.tips}</p>
        </div>
    `;
}


// Fertilizer Recommendation
document.getElementById('fertilizer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    const resultDiv = document.getElementById('fertilizer-result');
    resultDiv.innerHTML = '<div class="spinner"></div> Processing...';

    try {
        const response = await fetch('/api/fertilizer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        resultDiv.innerHTML = `
            <h4>Fertilizer Recommendation</h4>
            <p>${result.recommendation}</p>
            <p><strong>Application Method:</strong> ${result.method}</p>
        `;
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: var(--error)">Error: Could not get recommendation</p>`;
    }
});


// AI Chat Assistant
function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    const chatHistory = document.getElementById('chat-history');

    // User message
    const userMsg = document.createElement('div');
    userMsg.style.cssText = `
        padding: 8px 12px; margin: 4px 0; background-color: var(--primary); color: white;
        border-radius: 18px; max-width: 80%; align-self: flex-end; margin-left: auto;
    `;
    userMsg.textContent = message;
    chatHistory.appendChild(userMsg);

    input.value = '';

    // Typing indicator
    const typing = document.createElement('div');
    typing.id = 'typing-indicator';
    typing.style.cssText = `
        padding: 8px 12px; margin: 4px 0; background-color: rgba(46, 125, 50, 0.1);
        border-radius: 18px; max-width: 80%; display: flex;
    `;
    typing.innerHTML = '<div class="spinner" style="margin-right: 8px;"></div> Thinking...';
    chatHistory.appendChild(typing);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // AI response
    setTimeout(async () => {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const result = await response.json();
            document.getElementById('typing-indicator').remove();

            const aiMsg = document.createElement('div');
            aiMsg.style.cssText = `
                padding: 8px 12px; margin: 4px 0; background-color: rgba(46, 125, 50, 0.1);
                border-radius: 18px; max-width: 80%;
            `;
            aiMsg.textContent = result.reply;
            chatHistory.appendChild(aiMsg);

        } catch (error) {
            document.getElementById('typing-indicator').remove();
            const errorMsg = document.createElement('div');
            errorMsg.style.cssText = `
                padding: 8px 12px; margin: 4px 0; background-color: var(--error); color: white;
                border-radius: 18px; max-width: 80%;
            `;
            errorMsg.textContent = 'Sorry, I could not process your request.';
            chatHistory.appendChild(errorMsg);
        }
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }, 800);
}

// Allow Enter key to send chat message
document.getElementById('chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});
