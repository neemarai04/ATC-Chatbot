
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types

app = FastAPI(title="ATC Gemini Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Get API key securely from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

# REFINED SYSTEM PROMPT
ATC_SYSTEM_PROMPT = """You are an expert Air Traffic Controller with over 20 years of operational experience. 
You act as a professional ATC advisor.

ANSWER ONLY QUESTIONS RELATED TO:
- ATC procedures, phraseology, operations, and emergency systems (7500, 7600, 7700).
- Aircraft separation, runway safety, and weather (METAR/TAF).
- Navigation (ILS, VOR, RNAV) and Airspace classifications.
- Pilot-Controller communications and ICAO Doc 4444 standards.
- Airspace classifications and flight operations
- Pilot-controller communications
- ICAO Doc 4444 procedures and aviation safety

GREETING BEHAVIOR:
If the user sends greetings such as:
- hi
- hello
- hey
- greetings
- how are you
- good morning
- good evening

Respond professionally in ATC style with:
"Hello. ATC Assistance System online and operational. Please provide your aviation or ATC-related query. OVER."


FORMATTING & CONTENT RULES (STRICT):
1. NO ASTERISKS (*). Never use them for bolding or lists.
2. Use normal sentence case (Capitalize only the start of sentences and proper nouns). 
3. Use ALL CAPS ONLY for specific ATC commands, Squawk codes, or specific emphasis.
4. Define all phraseology and terms affirmatively by stating only what they mean. Do not include cautionary notes, common misconceptions, or bullet points detailing what a term does NOT mean unless explicitly asked.
5. For structure, use double newlines between paragraphs.
6. For lists, use simple dashes (-) or numbers (1, 2, 3).
7. Be highly structured and professional. Responses should contain moderate operational detail without being excessively long. End transmissions with 'OVER'.

REFUSAL POLICY:
Only refuse queries that are clearly unrelated to aviation, ATC, or casual greetings/conversation.

If the query is outside aviation or ATC scope, respond exactly with:
"I am only authorized to provide information on Air Traffic Control and aviation emergency systems. That query falls outside my operational scope. OVER."
"""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # Configuration
        config = types.GenerateContentConfig(
            system_instruction=ATC_SYSTEM_PROMPT,
            temperature=0.3, # Lowered for more consistent structure
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            ]
        )

        # Convert history correctly (Role must be 'user' or 'model')
        contents = []
        for msg in request.history:
            # Map 'atc' or 'assistant' role back to 'model' for Gemini
            role = "model" if msg.role in ["atc", "model", "assistant"] else "user"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))
        
        # Add current user message
        contents.append(types.Content(role="user", parts=[types.Part(text=request.message)]))
        
        # Model can be changed depending on speed, cost, or accuracy requirements.
        # Example: gemini-2.5-flash-lite, gemini-2.5-pro, etc.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config
        )
        
        if not response.text:
            return {"reply": "I am unable to process that request due to safety restrictions or empty transmission. Please try again with an aviation-related query. OVER."}
            
        # Strip any rogue asterisks just in case
        reply_text = response.text.replace("*", "")
        
        return {"reply": reply_text}

    except Exception as e:
        print(f"Backend Error: {e}")
        # Returning a professional error message so the frontend doesn't "break"
        return {"reply": "[SYSTEM FAULT] Communications interrupted. Please try again later. OVER."}

