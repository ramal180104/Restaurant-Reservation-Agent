# 🍽️ GoodFoods Reservation Assistant

GoodFoods Reservation Assistant is a rule-based conversational application that enables users to discover restaurant locations, receive personalized recommendations, and book table reservations through a structured and intuitive chat interface.

The system is designed with deterministic conversation flow, robust state management, and clean separation of concerns, making it suitable for production-style backend design and real-world use cases.

---

## 🚀 Features

- Search GoodFoods restaurants by **city**
- Filter restaurants by **cuisine**
- Get **personalized recommendations** based on:
  - Ambience (family, romantic, business, casual, rooftop)
  - Budget (low, medium, high)
- Guided **step-by-step reservation flow**
- Input validation and error handling
- Clear confirmation after successful reservation

---

## 🏙️ Supported Cities

- Hyderabad
- Bangalore
- Delhi

---

## 🍜 Supported Cuisines

- Indian
- Chinese
- Italian
- Mexican
- Cafe

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **Architecture:** Rule-based conversational state machine
- **Data Source:** In-memory restaurant dataset

---

## Architecture Overview

The GoodFoods Restaurant Reservation Agent follows a clean, layered architecture
with clear separation between UI, conversation control, business logic, and data.

### High-Level Flow

User  
⬇️  
Streamlit Frontend (Chat UI)  
⬇️  
FastAPI Backend (Conversation Controller)  
⬇️  
Business Logic Modules  
⬇️  
In-Memory Restaurant Dataset

### Component Breakdown

#### 1. Streamlit Frontend
- Handles user interaction and chat UI
- Displays questions and responses
- Sends user input to backend via HTTP

**Location:** `frontend/app.py`

---

#### 2. FastAPI Backend (Conversation Engine)
- Controls conversation flow and state
- Enforces one-question-at-a-time logic
- Validates inputs (city, ambience, budget, etc.)
- Routes requests to business logic modules

**Location:** `backend/main.py`

---

#### 3. Business Logic Modules
Stateless utility modules that perform core operations:

- **Search Module:** Filter restaurants by city and cuisine  
  `backend/tools/search.py`

- **Recommendation Module:** Suggest restaurants using ambience and budget  
  `backend/tools/recommend.py`

- **Reservation Module:** Confirm reservations after validation  
  `backend/tools/reserve.py`

---

#### 4. Data Layer
- In-memory mock dataset of GoodFoods restaurants
- Acts as the single source of truth for locations and attributes

**Location:** `backend/tools/data.py`

---

This architecture ensures:
- Deterministic behavior (no hallucinations)
- Clear separation of responsibilities
- Easy debugging and extensibility

---

## 🧠 Design Philosophy

- Deterministic behavior (no hallucinations)
- Backend-controlled conversation flow
- One question at a time for better UX
- No dependency on LLMs for core logic
- Easily extensible to voice bots or AI layers

---

## 🔄 Conversation Flow

1. User selects an intent (search / recommend / reserve)
2. City selection
3. Restaurant discovery or recommendation
4. Restaurant selection
5. Reservation details collection:
   - Party size
   - Date
   - Time
   - User name
6. Reservation confirmation

---

## ▶️ How to Run Locally

## 1. Clone the repository
git clone https://github.com/ramal180104/Restaurant-Reservation-Agent.git
cd Restaurant-Reservation-Agent

## 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

## (For Windows)
venv\Scripts\activate

## 3. Install dependencies
pip install -r requirements.txt

## If requirements.txt is not available
pip install fastapi uvicorn streamlit requests pydantic

## 4. Start the backend server (FastAPI)
uvicorn backend.main:app --port 8001

## Backend will run at
http://localhost:8001

## 5. Start the frontend (Streamlit)
Open a new terminal, activate the virtual environment again, then run:
streamlit run frontend/app.py

## Frontend will run at
http://localhost:8501

## 6. Stop the application
CTRL + C

## 7. Reset the conversation inside the app
Type: reset



