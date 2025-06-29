"""
Marketplace Configuration for Niche Business APIs Suite
Optimized for RapidAPI, AWS Marketplace, and other API marketplaces
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class PricingTier:
    name: str
    price: float
    requests_per_month: int
    features: List[str]
    rate_limit_per_minute: int

@dataclass
class APIConfig:
    name: str
    description: str
    category: str
    pricing_tiers: List[PricingTier]
    tags: List[str]
    documentation_url: str
    examples: List[Dict[str, Any]]

# Content Moderation API Configuration
CONTENT_MODERATION_CONFIG = APIConfig(
    name="Content Moderation API",
    description="Advanced content filtering and moderation for social media, forums, and user-generated content. Detect hate speech, spam, profanity, and inappropriate content with high accuracy.",
    category="Content Management",
    pricing_tiers=[
        PricingTier("Free", 0.0, 100, ["Basic moderation", "Hate speech detection"], 10),
        PricingTier("Basic", 9.99, 10000, ["Full moderation", "Spam detection", "Profanity filter"], 100),
        PricingTier("Pro", 29.99, 100000, ["Advanced features", "Custom rules", "Batch processing"], 500),
        PricingTier("Ultra", 99.99, 1000000, ["Enterprise features", "Priority support", "Custom models"], 2000)
    ],
    tags=["content-moderation", "hate-speech", "spam-detection", "profanity-filter", "social-media"],
    documentation_url="https://docs.example.com/content-moderation",
    examples=[
        {
            "title": "Moderate Social Media Post",
            "description": "Check if a social media post contains inappropriate content",
            "request": {
                "text": "This is a test post that should be checked for inappropriate content.",
                "content_type": "social_media",
                "strictness": "medium"
            },
            "response": {
                "is_appropriate": True,
                "confidence_score": 0.95,
                "flagged_issues": [],
                "risk_level": "low"
            }
        }
    ]
)

# Email Validation API Configuration
EMAIL_VALIDATION_CONFIG = APIConfig(
    name="Email Validation & Deliverability API",
    description="Comprehensive email validation and deliverability checking. Verify email formats, check MX records, detect disposable emails, and assess deliverability scores.",
    category="Email Marketing",
    pricing_tiers=[
        PricingTier("Free", 0.0, 1000, ["Basic validation", "Format checking"], 50),
        PricingTier("Basic", 4.99, 50000, ["Full validation", "MX checking", "Disposable detection"], 200),
        PricingTier("Pro", 19.99, 500000, ["Advanced features", "Role account detection", "Batch processing"], 1000),
        PricingTier("Ultra", 79.99, 5000000, ["Enterprise features", "Custom rules", "Priority support"], 5000)
    ],
    tags=["email-validation", "deliverability", "mx-check", "spam-prevention", "email-marketing"],
    documentation_url="https://docs.example.com/email-validation",
    examples=[
        {
            "title": "Validate Email Address",
            "description": "Check if an email address is valid and deliverable",
            "request": {
                "email": "user@example.com",
                "check_deliverability": True,
                "check_disposable": True
            },
            "response": {
                "is_valid": True,
                "is_deliverable": True,
                "confidence_score": 0.95,
                "domain_exists": True
            }
        }
    ]
)

# Crypto Analytics API Configuration
CRYPTO_ANALYTICS_CONFIG = APIConfig(
    name="Cryptocurrency Portfolio Analytics API",
    description="Advanced cryptocurrency portfolio analysis and risk assessment. Get portfolio performance metrics, diversification analysis, and investment recommendations.",
    category="Finance",
    pricing_tiers=[
        PricingTier("Free", 0.0, 100, ["Basic portfolio analysis", "Performance metrics"], 10),
        PricingTier("Basic", 14.99, 5000, ["Full analysis", "Risk assessment", "Diversification scoring"], 100),
        PricingTier("Pro", 49.99, 50000, ["Advanced features", "Market overview", "Custom metrics"], 500),
        PricingTier("Ultra", 199.99, 500000, ["Enterprise features", "Real-time data", "Priority support"], 2000)
    ],
    tags=["cryptocurrency", "portfolio-analysis", "risk-assessment", "investment", "crypto-trading"],
    documentation_url="https://docs.example.com/crypto-analytics",
    examples=[
        {
            "title": "Analyze Portfolio",
            "description": "Analyze a cryptocurrency portfolio for performance and risk",
            "request": {
                "assets": [
                    {"symbol": "BTC", "quantity": 1.5, "purchase_price": 40000, "purchase_date": "2024-01-01"},
                    {"symbol": "ETH", "quantity": 10, "purchase_price": 3000, "purchase_date": "2024-01-01"}
                ]
            },
            "response": {
                "total_value": 67500,
                "total_profit_loss": 1500,
                "profit_loss_percentage": 2.27,
                "risk_level": "medium"
            }
        }
    ]
)

# Sentiment Analysis API Configuration
SENTIMENT_ANALYSIS_CONFIG = APIConfig(
    name="Social Media Sentiment Analysis API",
    description="Advanced sentiment analysis and emotion detection for social media monitoring and brand analysis. Extract insights from text with high accuracy.",
    category="Analytics",
    pricing_tiers=[
        PricingTier("Free", 0.0, 100, ["Basic sentiment analysis", "Positive/negative scoring"], 10),
        PricingTier("Basic", 9.99, 10000, ["Full analysis", "Emotion detection", "Keyword extraction"], 100),
        PricingTier("Pro", 29.99, 100000, ["Advanced features", "Batch processing", "Custom models"], 500),
        PricingTier("Ultra", 99.99, 1000000, ["Enterprise features", "Real-time analysis", "Priority support"], 2000)
    ],
    tags=["sentiment-analysis", "emotion-detection", "social-media", "brand-monitoring", "text-analysis"],
    documentation_url="https://docs.example.com/sentiment-analysis",
    examples=[
        {
            "title": "Analyze Social Media Post",
            "description": "Analyze sentiment and emotions in a social media post",
            "request": {
                "text": "I absolutely love this new product! It's amazing and works perfectly.",
                "include_emotions": True,
                "include_keywords": True
            },
            "response": {
                "sentiment_score": 0.8,
                "sentiment_label": "positive",
                "confidence": 0.95,
                "emotions": {"joy": 0.8, "trust": 0.6}
            }
        }
    ]
)

# PDF Processing API Configuration
PDF_PROCESSING_CONFIG = APIConfig(
    name="PDF Document Processing API",
    description="Advanced PDF document analysis and data extraction. Extract text, tables, metadata, and insights from PDF documents with high accuracy.",
    category="Document Processing",
    pricing_tiers=[
        PricingTier("Free", 0.0, 10, ["Basic text extraction", "Page count"], 5),
        PricingTier("Basic", 19.99, 1000, ["Full extraction", "Table detection", "Metadata analysis"], 50),
        PricingTier("Pro", 49.99, 10000, ["Advanced features", "Keyword extraction", "Entity detection"], 200),
        PricingTier("Ultra", 199.99, 100000, ["Enterprise features", "Custom extraction", "Priority support"], 1000)
    ],
    tags=["pdf-processing", "document-analysis", "text-extraction", "table-detection", "data-extraction"],
    documentation_url="https://docs.example.com/pdf-processing",
    examples=[
        {
            "title": "Extract Text from PDF",
            "description": "Extract and analyze text content from a PDF document",
            "request": {
                "file": "document.pdf",
                "extract_text": True,
                "extract_tables": True,
                "extract_metadata": True
            },
            "response": {
                "page_count": 5,
                "word_count": 1250,
                "tables_found": 2,
                "keywords": ["business", "strategy", "analysis"]
            }
        }
    ]
)

# Weather Business Intelligence API Configuration
WEATHER_BI_CONFIG = APIConfig(
    name="Weather Business Intelligence API",
    description="Weather-driven business intelligence and decision support. Analyze weather impact on retail, agriculture, logistics, and tourism businesses.",
    category="Business Intelligence",
    pricing_tiers=[
        PricingTier("Free", 0.0, 100, ["Basic weather analysis", "Current conditions"], 10),
        PricingTier("Basic", 9.99, 10000, ["Full analysis", "Business impact", "Recommendations"], 100),
        PricingTier("Pro", 29.99, 100000, ["Advanced features", "Seasonal analysis", "Risk assessment"], 500),
        PricingTier("Ultra", 99.99, 1000000, ["Enterprise features", "Custom models", "Priority support"], 2000)
    ],
    tags=["weather", "business-intelligence", "retail", "agriculture", "logistics"],
    documentation_url="https://docs.example.com/weather-business",
    examples=[
        {
            "title": "Analyze Retail Weather Impact",
            "description": "Analyze weather impact on retail business operations",
            "request": {
                "location": "New York",
                "business_type": "retail",
                "forecast_days": 7
            },
            "response": {
                "sales_forecast": "high",
                "product_recommendations": ["summer clothing", "beverages"],
                "risk_level": "low",
                "recommendations": ["Increase inventory of weather-appropriate products"]
            }
        }
    ]
)

# All API configurations
ALL_APIS = {
    "content-moderation": CONTENT_MODERATION_CONFIG,
    "email-validation": EMAIL_VALIDATION_CONFIG,
    "crypto-analytics": CRYPTO_ANALYTICS_CONFIG,
    "sentiment-analysis": SENTIMENT_ANALYSIS_CONFIG,
    "pdf-processing": PDF_PROCESSING_CONFIG,
    "weather-business": WEATHER_BI_CONFIG
}

def get_api_config(api_name: str) -> APIConfig:
    """Get configuration for a specific API"""
    return ALL_APIS.get(api_name)

def get_all_configs() -> Dict[str, APIConfig]:
    """Get all API configurations"""
    return ALL_APIS

def generate_marketplace_listing(api_name: str) -> Dict[str, Any]:
    """Generate marketplace listing data for an API"""
    config = get_api_config(api_name)
    if not config:
        return {}
    
    return {
        "name": config.name,
        "description": config.description,
        "category": config.category,
        "tags": config.tags,
        "pricing": [
            {
                "tier": tier.name,
                "price": tier.price,
                "requests_per_month": tier.requests_per_month,
                "features": tier.features,
                "rate_limit": tier.rate_limit_per_minute
            }
            for tier in config.pricing_tiers
        ],
        "documentation_url": config.documentation_url,
        "examples": config.examples
    } 