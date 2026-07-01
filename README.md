# ATC Gemini Assistant API

An AI-powered Air Traffic Control (ATC) assistant backend developed using FastAPI and Google Gemini API.  
The system is designed to provide professional aviation and ATC-related assistance with structured, operational-style responses.

---

## Features


* AI-powered chatbot interface
* Retrieval-Augmented Generation (RAG)
* Context-aware ATC query responses
* Interactive frontend dashboard
* Fast and responsive UI
* Backend integration using Python

---

## Technologies Used

- Python
- FastAPI
- Google Gemini API
- Pydantic
- React
- vite
- JavaScript
- CSS

---

## Installation

### Clone the Repository

```bash
git clone "https://github.com/neemarai04/ATC-Chatbot.git"
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


## Model Configuration

The project currently uses:

```python
model="gemini-2.5-flash"
```

You may replace it with any supported Gemini model based on performance or deployment requirements.

---

## Project Scope

This project is intended for:
- Educational purposes
- Research and experimentation
- ATC communication assistance simulations
- Aviation-related AI applications

The assistant is restricted to aviation and ATC-related topics only.

---
## Future Improvements

* Improved conversational accuracy
* Better context retrieval
* Voice input support
* Real-time ATC stream integration
* Enhanced NLP processing

---
## Author

Neema J Rai
