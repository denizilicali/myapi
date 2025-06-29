from fastapi import FastAPI
from apis import (
    summarize_api, iban_api, qr_api, currency_api,
    content_moderation_api, crypto_analytics_api, email_validation_api,
    sentiment_analysis_api, pdf_processing_api, weather_business_api
)

app = FastAPI(
    title="Niche Business APIs Suite",
    description="A comprehensive suite of niche APIs for passive income generation",
    version="2.0.0"
)

# Include all API routers
app.include_router(summarize_api.router, prefix="/summarize", tags=["Text Summarization"])
app.include_router(iban_api.router, prefix="/iban", tags=["IBAN Validation"])
app.include_router(qr_api.router, prefix="/qr", tags=["QR Code Generation"])
app.include_router(currency_api.router, prefix="/currency", tags=["Currency Conversion"])

# New niche APIs
app.include_router(content_moderation_api.router, prefix="/content-moderation", tags=["Content Moderation"])
app.include_router(crypto_analytics_api.router, prefix="/crypto-analytics", tags=["Cryptocurrency Analytics"])
app.include_router(email_validation_api.router, prefix="/email-validation", tags=["Email Validation"])
app.include_router(sentiment_analysis_api.router, prefix="/sentiment-analysis", tags=["Sentiment Analysis"])
app.include_router(pdf_processing_api.router, prefix="/pdf-processing", tags=["PDF Processing"])
app.include_router(weather_business_api.router, prefix="/weather-business", tags=["Weather Business Intelligence"])

@app.get("/")
async def root():
    return {
        "message": "Niche Business APIs Suite is running!",
        "version": "2.0.0",
        "available_apis": [
            "Text Summarization",
            "IBAN Validation", 
            "QR Code Generation",
            "Currency Conversion",
            "Content Moderation",
            "Cryptocurrency Analytics",
            "Email Validation",
            "Sentiment Analysis",
            "PDF Processing",
            "Weather Business Intelligence"
        ],
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Overall health check for all services"""
    return {
        "status": "healthy",
        "services": [
            "summarize_api",
            "iban_api", 
            "qr_api",
            "currency_api",
            "content_moderation_api",
            "crypto_analytics_api",
            "email_validation_api",
            "sentiment_analysis_api",
            "pdf_processing_api",
            "weather_business_api"
        ]
    }
