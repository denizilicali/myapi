from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class TextRequest(BaseModel):
    text: str

@router.post("/")
async def summarize_text(request: TextRequest):
    text = request.text
    if len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return {"summary": summary[0]['summary_text']}

