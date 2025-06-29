from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import re
from textblob import TextBlob
from datetime import datetime
import statistics

router = APIRouter()

class SentimentAnalysisRequest(BaseModel):
    text: str
    language: str = "en"
    include_emotions: bool = True
    include_keywords: bool = True

class SentimentAnalysisResponse(BaseModel):
    text: str
    sentiment_score: float
    sentiment_label: str  # positive, negative, neutral
    confidence: float
    emotions: Dict[str, float]
    keywords: List[Dict[str, Any]]
    analysis_details: Dict[str, Any]

class BatchSentimentRequest(BaseModel):
    texts: List[str]
    language: str = "en"
    include_emotions: bool = True
    include_keywords: bool = True

# Emotion keywords and their weights
EMOTION_KEYWORDS = {
    "joy": ["happy", "excited", "great", "amazing", "wonderful", "fantastic", "love", "enjoy", "pleased", "thrilled"],
    "sadness": ["sad", "depressed", "unhappy", "miserable", "disappointed", "heartbroken", "grief", "sorrow", "melancholy"],
    "anger": ["angry", "furious", "mad", "irritated", "annoyed", "frustrated", "outraged", "livid", "enraged"],
    "fear": ["scared", "afraid", "terrified", "worried", "anxious", "nervous", "frightened", "panicked", "horrified"],
    "surprise": ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered", "startled"],
    "disgust": ["disgusted", "revolted", "sickened", "appalled", "repulsed", "nauseated"],
    "trust": ["trust", "confident", "reliable", "faithful", "loyal", "dependable", "secure"],
    "anticipation": ["excited", "eager", "hopeful", "optimistic", "enthusiastic", "looking forward"]
}

# Sentiment modifiers
INTENSIFIERS = ["very", "extremely", "really", "so", "too", "absolutely", "completely"]
NEGATORS = ["not", "no", "never", "none", "neither", "nor", "doesn't", "don't", "isn't", "aren't", "wasn't", "weren't"]

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment label
    if polarity > 0.1:
        sentiment_label = "positive"
    elif polarity < -0.1:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"
    
    # Calculate confidence based on subjectivity
    confidence = abs(polarity) * (1 - subjectivity) + subjectivity * 0.5
    
    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "sentiment_label": sentiment_label,
        "confidence": min(1.0, confidence)
    }

def extract_emotions(text: str) -> Dict[str, float]:
    """Extract emotions from text"""
    text_lower = text.lower()
    emotions = {}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count occurrences with word boundaries
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            score += matches
        
        # Normalize score
        if score > 0:
            emotions[emotion] = min(1.0, score / 3.0)  # Cap at 1.0
    
    return emotions

def extract_keywords(text: str) -> List[Dict[str, Any]]:
    """Extract important keywords from text"""
    blob = TextBlob(text)
    
    # Get noun phrases and important words
    keywords = []
    
    # Extract noun phrases
    for phrase in blob.noun_phrases:
        if len(phrase) > 2:  # Filter out very short phrases
            keywords.append({
                "text": phrase,
                "type": "noun_phrase",
                "importance": len(phrase.split()) * 0.5
            })
    
    # Extract important words (nouns, adjectives, verbs)
    for word, tag in blob.tags:
        if tag.startswith(('NN', 'JJ', 'VB')) and len(word) > 2:
            importance = 1.0
            if tag.startswith('NN'):  # Nouns
                importance = 1.2
            elif tag.startswith('JJ'):  # Adjectives
                importance = 1.0
            elif tag.startswith('VB'):  # Verbs
                importance = 0.8
            
            keywords.append({
                "text": word,
                "type": tag,
                "importance": importance
            })
    
    # Remove duplicates and sort by importance
    unique_keywords = {}
    for kw in keywords:
        text = kw["text"].lower()
        if text not in unique_keywords or kw["importance"] > unique_keywords[text]["importance"]:
            unique_keywords[text] = kw
    
    return sorted(unique_keywords.values(), key=lambda x: x["importance"], reverse=True)[:10]

def analyze_text_complexity(text: str) -> Dict[str, Any]:
    """Analyze text complexity and readability"""
    sentences = text.split('.')
    words = text.split()
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    # Count different types of words
    long_words = sum(1 for word in words if len(word) > 6)
    long_word_ratio = long_words / len(words) if words else 0
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_sentence_length": avg_sentence_length,
        "avg_word_length": avg_word_length,
        "long_word_ratio": long_word_ratio,
        "complexity_level": "high" if long_word_ratio > 0.2 else "medium" if long_word_ratio > 0.1 else "low"
    }

@router.post("/analyze", response_model=SentimentAnalysisResponse)
async def analyze_sentiment_endpoint(request: SentimentAnalysisRequest):
    """
    Analyze sentiment, emotions, and extract keywords from text.
    
    - **text**: Text to analyze
    - **language**: Language of the text (default: en)
    - **include_emotions**: Include emotion analysis
    - **include_keywords**: Include keyword extraction
    """
    try:
        # Basic sentiment analysis
        sentiment_result = analyze_sentiment(request.text)
        
        # Extract emotions if requested
        emotions = extract_emotions(request.text) if request.include_emotions else {}
        
        # Extract keywords if requested
        keywords = extract_keywords(request.text) if request.include_keywords else []
        
        # Analyze text complexity
        complexity = analyze_text_complexity(request.text)
        
        return SentimentAnalysisResponse(
            text=request.text,
            sentiment_score=sentiment_result["polarity"],
            sentiment_label=sentiment_result["sentiment_label"],
            confidence=sentiment_result["confidence"],
            emotions=emotions,
            keywords=keywords,
            analysis_details={
                "subjectivity": sentiment_result["subjectivity"],
                "complexity": complexity,
                "language": request.language,
                "analysis_timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@router.post("/batch-analyze")
async def batch_analyze_sentiment(request: BatchSentimentRequest):
    """
    Analyze sentiment for multiple texts at once.
    """
    try:
        results = []
        for text in request.texts:
            try:
                analysis_request = SentimentAnalysisRequest(
                    text=text,
                    language=request.language,
                    include_emotions=request.include_emotions,
                    include_keywords=request.include_keywords
                )
                result = await analyze_sentiment_endpoint(analysis_request)
                results.append(result.dict())
            except Exception as e:
                results.append({
                    "text": text,
                    "error": str(e),
                    "sentiment_score": 0,
                    "sentiment_label": "neutral"
                })
        
        # Calculate aggregate statistics
        sentiment_scores = [r.get("sentiment_score", 0) for r in results if "sentiment_score" in r]
        
        return {
            "results": results,
            "total_processed": len(request.texts),
            "aggregate_stats": {
                "avg_sentiment": statistics.mean(sentiment_scores) if sentiment_scores else 0,
                "sentiment_std": statistics.stdev(sentiment_scores) if len(sentiment_scores) > 1 else 0,
                "positive_count": sum(1 for r in results if r.get("sentiment_label") == "positive"),
                "negative_count": sum(1 for r in results if r.get("sentiment_label") == "negative"),
                "neutral_count": sum(1 for r in results if r.get("sentiment_label") == "neutral")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.get("/emotions")
async def get_available_emotions():
    """Get list of available emotions for analysis"""
    return {
        "available_emotions": list(EMOTION_KEYWORDS.keys()),
        "emotion_keywords": EMOTION_KEYWORDS
    }

@router.get("/health")
async def health_check():
    """Health check endpoint for the sentiment analysis service"""
    return {"status": "healthy", "service": "sentiment_analysis"} 