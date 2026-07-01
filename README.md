# ATC Chatbot

An AI-powered Air Traffic Control (ATC) assistant developed during an internship under the EMBRACE initiative at NITK Surathkal. 
The application provides domain-specific assistance for aviation and ATC-related queries using Google Gemini, delivering structured and professional responses through a FastAPI backend and a React-based frontend.

---

## Features

* AI-powered aviation and ATC assistant
* Context-aware responses for ATC and aviation queries
* FastAPI backend for efficient request handling
* Interactive React dashboard
* Responsive user interface
* Domain-restricted conversations focused on aviation and ATC

---

## Technologies Used

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Google Gemini API
* Pydantic

---

## Project Structure

```text
ATC-Chatbot/
│
├── main.py
├── requirements.txt
├── .env
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
```

---

## Installation

### Clone the Repository

```bash
git clone "https://github.com/neemarai04/ATC-Chatbot.git"
cd ATC-Chatbot
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The application securely loads the API key using environment variables.

---

## Running the Application

### Start the Backend

From the project root directory:

```bash
uvicorn main:app --reload
```

### Start the Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

### Open in Browser

After starting the frontend, open the local URL shown in the terminal (usually `http://localhost:5173`).

---

## Model Configuration

The project currently uses:

```python
model="gemini-2.5-flash"
```

You may replace it with any supported Gemini model based on performance or deployment requirements.

---

## Project Scope

This project is intended for:
* Educational purposes
* Research and experimentation
* ATC communication assistance simulations
* Aviation-related AI applications

The assistant is restricted to aviation and ATC-related topics only.

---

## Future Improvements

* Improved conversational accuracy
* Better context retrieval
* Voice-based interaction
* Integration with live ATC transcription systems
* Support for aviation document search
* Multi-turn conversation memory

---

## Author

Neema J Rai
