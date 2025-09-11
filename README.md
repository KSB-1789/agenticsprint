```
# 🚀 AgenticSprint Prototype

An AI-powered assistant prototype built for **AgenticSprint: From Prototype to Future Tech** (Hackathon, Sept 15–17).  
This project demonstrates a simple **frontend (Streamlit)** connected to a **backend (FastAPI)**, ready for integration with AI models.

---
## 📂 Project Structure
## 📂 Project Structure
```

.
├── app.py           # Streamlit frontend (chat UI)
├── backend.py       # FastAPI backend (dummy AI response)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <repo-link>
cd <repo-folder>
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

### Start Backend (Terminal 1)

```bash
uvicorn backend:app --reload
```

### Start Frontend (Terminal 2)

```bash
streamlit run app.py
```

The app will open automatically at:
👉 [http://localhost:8501](http://localhost:8501)

---

## 💡 Features

* 🖥️ **Frontend:** Chat-style UI built with Streamlit
* ⚙️ **Backend:** FastAPI service (currently dummy AI response)
* 🔗 **Integration:** Streamlit calls backend API for answers
* 🎯 **Hackathon Ready:** Easy to extend with real AI models (Kritika’s part)

---

## 🔄 Demo Modes

The project supports **two demo modes** (to avoid failure during judging):

1. **Real Mode:** Connects to backend API (FastAPI with AI model).
2. **Dummy Mode:** Uses placeholder response (safe fallback if backend fails).

---

## 👩‍💻 Team Roles

* **Karanveer Singh** – Frontend, repo, documentation, pitch
* **Kritika** – Backend AI integration (RTX 3050)
* **Eknoor** – Mac demo setup, presentation polish

---

## 🌟 Next Steps

* Replace dummy backend with AI pipeline (LLMs + vector DB).
* Add memory + multi-agent orchestration.
* Deploy final version for hackathon demo.

```

---


