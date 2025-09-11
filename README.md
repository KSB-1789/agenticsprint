🚀 AgenticSprint Prototype
An AI-powered assistant prototype built for AgenticSprint: From Prototype to Future Tech (Hackathon, Sept 15–17).This project demonstrates a simple frontend (Streamlit) connected to a backend (FastAPI), ready for integration with AI models.
📂 Project Structure
.
├── app.py               # Streamlit frontend (chat UI)
├── backend/             # FastAPI backend (AI logic, API routes)
│   ├── main.py          # FastAPI app entrypoint
│   ├── ai.py            # AI model integration
│   └── utils.py         # Helper functions
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone <repo-link>
cd <repo-folder>

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the App

Start Backend (Terminal 1)

uvicorn backend.main:app --reload


Start Frontend (Terminal 2)

streamlit run app.py

The app will open automatically at:👉 http://localhost:8501
💡 Features

🖥️ Frontend: Chat-style UI built with Streamlit
⚙️ Backend: FastAPI service (AI model integration)
🔗 Integration: Streamlit calls backend API for answers
🎯 Hackathon Ready: Modular, easy to extend

🔄 Demo Modes
The project supports two demo modes:

Real Mode: Connects to backend API (FastAPI with AI model).
Dummy Mode: Uses placeholder response (safe fallback if backend fails).

👩‍💻 Team Roles

Karanveer Singh: Frontend, repo, documentation, pitch
Kritika: Backend AI integration (RTX 3050)
Eknoor: Mac demo setup, presentation polish

🌟 Next Steps

Integrate advanced AI pipeline (LLMs + vector DB)
Add memory + multi-agent orchestration
Deploy final version for hackathon demo
