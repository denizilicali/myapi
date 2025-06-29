from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import re
import json

router = APIRouter()

class ContentModerationRequest(BaseModel):
    text: str
    content_type: str = "general"  # general, social_media, forum, comments
    strictness: str = "medium"  # low, medium, high

class ContentModerationResponse(BaseModel):
    is_appropriate: bool
    confidence_score: float
    flagged_issues: List[str]
    risk_level: str  # low, medium, high, critical
    suggested_action: str
    moderation_details: Dict[str, Any]

# Predefined patterns for content moderation
HATE_SPEECH_PATTERNS = [
    r'\b(kill|murder|death)\s+(all|every)\s+(black|white|jew|muslim|gay|trans)\w*\b',
    r'\b(hitler|nazi|supremacy|genocide)\b',
    r'\b(rape|pedo|child\s+molest)\w*\b',
    r'\b(bomb|terrorist|attack)\s+(all|every)\s+\w+\b'
]

SPAM_PATTERNS = [
    r'\b(buy\s+now|limited\s+time|act\s+fast|click\s+here)\b',
    r'\b(free\s+offer|money\s+back|guaranteed|no\s+risk)\b',
    r'\b(earn\s+\$\d+|\d+\%\s+off|discount|sale)\b',
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
]

PROFANITY_PATTERNS = [
    r'\b(fuck|shit|bitch|asshole|dick|pussy|cunt)\w*\b',
    r'\b(motherfucker|fucker|bastard|whore|slut)\w*\b'
]

def analyze_content(text: str, content_type: str, strictness: str) -> Dict[str, Any]:
    """Analyze content for inappropriate material"""
    text_lower = text.lower()
    issues = []
    risk_score = 0
    
    # Check for hate speech
    for pattern in HATE_SPEECH_PATTERNS:
        if re.search(pattern, text_lower):
            issues.append("hate_speech")
            risk_score += 0.8
    
    # Check for spam
    spam_count = 0
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            spam_count += 1
    
    if spam_count >= 2:
        issues.append("spam")
        risk_score += 0.6
    
    # Check for profanity
    profanity_count = 0
    for pattern in PROFANITY_PATTERNS:
        matches = re.findall(pattern, text_lower)
        profanity_count += len(matches)
    
    if profanity_count > 0:
        issues.append("profanity")
        risk_score += 0.3 * min(profanity_count, 3)
    
    # Check for excessive caps (shouting)
    caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
    if caps_ratio > 0.7 and len(text) > 10:
        issues.append("excessive_caps")
        risk_score += 0.2
    
    # Adjust based on strictness
    if strictness == "high":
        risk_score *= 1.5
    elif strictness == "low":
        risk_score *= 0.7
    
    # Determine risk level
    if risk_score >= 0.8:
        risk_level = "critical"
        suggested_action = "block"
    elif risk_score >= 0.6:
        risk_level = "high"
        suggested_action = "flag_for_review"
    elif risk_score >= 0.4:
        risk_level = "medium"
        suggested_action = "warn"
    else:
        risk_level = "low"
        suggested_action = "allow"
    
    return {
        "is_appropriate": risk_score < 0.6,
        "confidence_score": min(1.0, risk_score),
        "flagged_issues": issues,
        "risk_level": risk_level,
        "suggested_action": suggested_action,
        "moderation_details": {
            "hate_speech_detected": "hate_speech" in issues,
            "spam_detected": "spam" in issues,
            "profanity_count": profanity_count,
            "caps_ratio": caps_ratio,
            "text_length": len(text),
            "content_type": content_type,
            "strictness_level": strictness
        }
    }

@router.post("/moderate", response_model=ContentModerationResponse)
async def moderate_content(request: ContentModerationRequest):
    """
    Moderate content for inappropriate material, hate speech, and spam.
    
    - **text**: The content to moderate
    - **content_type**: Type of content (general, social_media, forum, comments)
    - **strictness**: Moderation strictness level (low, medium, high)
    """
    try:
        result = analyze_content(request.text, request.content_type, request.strictness)
        return ContentModerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Moderation failed: {str(e)}")

@router.post("/batch-moderate")
async def batch_moderate_content(texts: List[str], content_type: str = "general", strictness: str = "medium"):
    """
    Moderate multiple pieces of content at once for efficiency.
    """
    try:
        results = []
        for text in texts:
            result = analyze_content(text, content_type, strictness)
            results.append({
                "text": text[:100] + "..." if len(text) > 100 else text,
                "moderation_result": result
            })
        return {"results": results, "total_processed": len(texts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch moderation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the content moderation service"""
    return {"status": "healthy", "service": "content_moderation"} 