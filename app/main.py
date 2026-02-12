
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import os
from model import predict_visa

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if API_KEY:
    genai.configure(api_key=API_KEY)
    gemini_model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        generation_config={"temperature": 0.3, "max_output_tokens": 1000}
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(
    age: int = Form(...),
    visa_type: str = Form(...),
    applied_month: int = Form(...),
    financial_status: int = Form(...),
    nationality: str = Form(...),
    destination_country: str = Form(...),
    experience: int = Form(...),
    education_level: int = Form(...),
    previous_rejections: int = Form(...)
):

    status, processing_time, confidence = predict_visa(
        age, visa_type, applied_month,
        financial_status, experience,
        education_level, previous_rejections
    )

    explanation = "Gemini API key not configured."

    if gemini_model:
        prompt = f"""
You are an enterprise AI Visa Decision Analyst.

Applicant:
Age: {age}
Visa Type: {visa_type}
Applied Month: {applied_month}
Financial Strength: {financial_status}
Nationality: {nationality}
Destination: {destination_country}
Experience: {experience}
Education: {education_level}
Previous Rejections: {previous_rejections}

ML Output:
Status: {status}
Processing Time: {processing_time} days
Confidence: {confidence}%

Provide:
1. Analytical reasoning
2. Risk vs strength breakdown
3. Processing time reasoning
4. Strategic improvement guidance
Professional tone.
"""
        try:
            response = gemini_model.generate_content(prompt)
            explanation = response.text.strip()
        except:
            explanation = "AI explanation temporarily unavailable."

    return {
        "visa_status": status,
        "processing_days": processing_time,
        "confidence": confidence,
        "ai_explanation": explanation
    }
