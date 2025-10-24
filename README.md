🌾 Krishi Sevak – Smart Agriculture Web App

Krishi Sevak is a modern, responsive web application built to assist Indian farmers using technology and AI.
It combines crop recommendation, disease detection, weather forecasting, mandi (market) prices, fertilizer advice, and an AI-powered chat assistant — all within a clean and mobile-friendly interface.

🚀 Features
🌱 Crop Recommendation

Predicts the most suitable crop to grow based on soil type and season using AI-backed backend APIs.

🍃 Disease Detection

Upload a crop leaf image to detect possible plant diseases and receive recommended solutions.

🌦️ Weather Forecast

Displays real-time weather and 7-day forecast for major Indian cities (Agra, Delhi, Mumbai, etc.).

🏪 Mandi Prices

Shows latest market prices of agricultural commodities from AGMARKNET and other sources.

🌾 Crop Information Lookup

Quickly access vital information like season, water requirement, temperature range, and farming tips for major crops.

💧 Fertilizer Recommendation

Get AI-based fertilizer usage suggestions and best application methods for specific crops.

🤖 AI Chat Assistant

An integrated chatbot that answers farming-related questions, from weather to pest management, using your backend’s AI model.

🌓 Light & Dark Mode

Built-in theme switcher with state saved in localStorage — elegant in both modes.

🛠️ Tech Stack
Layer	Technology
Frontend	HTML5, CSS3, JavaScript (Vanilla JS)
Design System	Custom UI with modern CSS grid/flexbox, responsive layouts
Theme	Light/Dark modes using CSS variables
APIs (expected)	/api/recommend, /api/detect, /api/weather, /api/mandi, /api/fertilizer, /api/chat
Backend (optional)	Flask / Node.js (depending on your setup)
📁 Project Structure
krishi-sevak/
│
├── index.html          # Main UI structure
├── static/
│   ├── css/
│   │   └── style.css   # Styling and theme definitions
│   └── js/
│       └── app.js      # All app logic and API integration
└── manifest.json       # For PWA (installable web app)

🧠 How It Works

The app loads with a dashboard showing system status.

Farmers can navigate between modules using the sidebar.

Each module uses JavaScript fetch() to communicate with backend APIs.

Data such as crop suggestions, weather, and prices are dynamically rendered into the UI.

The chat assistant allows conversational interaction powered by your AI model.

💡 Highlights

Fully responsive design (desktop + mobile)

Progressive Web App (PWA) ready

Minimal dependencies — no external JS frameworks

Smooth transitions, polished typography, and accessibility-aware layout

🔧 Setup Instructions

Clone the repository:

git clone https://github.com/yourusername/krishi-sevak.git
cd krishi-sevak


Serve the files locally:

python -m http.server 8000


or use any local static server (e.g., live-server in VSCode).

Connect the frontend to your backend endpoints (/api/...) by adjusting API URLs in app.js if needed.

Open in browser:
👉 http://localhost:8000

🤝 Contributing

Contributions, bug reports, and suggestions are welcome!
Open an issue or submit a pull request to help improve Krishi Sevak.

📜 License

This project is released under the MIT License.
Feel free to use, modify, and distribute for educational or social good purposes.

❤️ Acknowledgments

Developed with passion for Indian farmers 🇮🇳
Empowering agriculture through data, AI, and open-source technology
