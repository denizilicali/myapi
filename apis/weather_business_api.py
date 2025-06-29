from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests
from datetime import datetime, timedelta
import statistics

router = APIRouter()

class WeatherBusinessRequest(BaseModel):
    location: str
    business_type: str  # retail, agriculture, logistics, tourism, construction
    analysis_type: str = "general"  # general, seasonal, impact_analysis
    forecast_days: int = 7

class WeatherBusinessResponse(BaseModel):
    location: str
    business_type: str
    current_weather: Dict[str, Any]
    business_impact: Dict[str, Any]
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    forecast_analysis: Dict[str, Any]

class SeasonalAnalysisRequest(BaseModel):
    location: str
    business_type: str
    season: str  # spring, summer, fall, winter
    year: int = datetime.now().year

# Mock weather data (in real implementation, use OpenWeatherMap, WeatherAPI, etc.)
MOCK_WEATHER_DATA = {
    "New York": {
        "current": {"temp": 22, "humidity": 65, "wind_speed": 12, "condition": "partly_cloudy"},
        "forecast": [
            {"date": "2024-01-15", "temp": 20, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-16", "temp": 18, "condition": "rainy", "precipitation": 15},
            {"date": "2024-01-17", "temp": 25, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-18", "temp": 22, "condition": "cloudy", "precipitation": 5},
            {"date": "2024-01-19", "temp": 19, "condition": "stormy", "precipitation": 25},
            {"date": "2024-01-20", "temp": 21, "condition": "partly_cloudy", "precipitation": 2},
            {"date": "2024-01-21", "temp": 24, "condition": "sunny", "precipitation": 0}
        ]
    },
    "Los Angeles": {
        "current": {"temp": 28, "humidity": 45, "wind_speed": 8, "condition": "sunny"},
        "forecast": [
            {"date": "2024-01-15", "temp": 26, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-16", "temp": 27, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-17", "temp": 29, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-18", "temp": 25, "condition": "cloudy", "precipitation": 0},
            {"date": "2024-01-19", "temp": 26, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-20", "temp": 28, "condition": "sunny", "precipitation": 0},
            {"date": "2024-01-21", "temp": 30, "condition": "sunny", "precipitation": 0}
        ]
    }
}

def get_weather_data(location: str) -> Dict[str, Any]:
    """Get weather data for location (mock implementation)"""
    # In real implementation, call weather API
    return MOCK_WEATHER_DATA.get(location, MOCK_WEATHER_DATA["New York"])

def analyze_retail_impact(weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze weather impact on retail business"""
    current = weather_data["current"]
    forecast = weather_data["forecast"]
    
    # Temperature impact
    temp_impact = "neutral"
    if current["temp"] > 30:
        temp_impact = "negative"  # Too hot, people stay inside
    elif current["temp"] < 5:
        temp_impact = "negative"  # Too cold, people stay inside
    elif 15 <= current["temp"] <= 25:
        temp_impact = "positive"  # Comfortable weather for shopping
    
    # Precipitation impact
    precip_impact = "negative" if current["condition"] in ["rainy", "stormy"] else "positive"
    
    # Product recommendations based on weather
    product_recommendations = []
    if current["temp"] > 25:
        product_recommendations.extend(["summer clothing", "beverages", "sunscreen", "outdoor items"])
    elif current["temp"] < 10:
        product_recommendations.extend(["winter clothing", "hot beverages", "indoor entertainment"])
    
    if current["condition"] in ["rainy", "stormy"]:
        product_recommendations.extend(["umbrellas", "rain gear", "indoor activities"])
    
    # Sales forecast
    sales_forecast = "stable"
    if temp_impact == "positive" and precip_impact == "positive":
        sales_forecast = "high"
    elif temp_impact == "negative" or precip_impact == "negative":
        sales_forecast = "low"
    
    return {
        "temperature_impact": temp_impact,
        "precipitation_impact": precip_impact,
        "product_recommendations": product_recommendations,
        "sales_forecast": sales_forecast,
        "customer_traffic": "high" if sales_forecast == "high" else "low" if sales_forecast == "low" else "normal"
    }

def analyze_agriculture_impact(weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze weather impact on agriculture"""
    current = weather_data["current"]
    forecast = weather_data["forecast"]
    
    # Temperature analysis
    temp_analysis = "optimal"
    if current["temp"] > 35:
        temp_analysis = "stress"  # Heat stress
    elif current["temp"] < 0:
        temp_analysis = "frost_risk"
    
    # Precipitation analysis
    total_precip = sum(day["precipitation"] for day in forecast)
    precip_analysis = "adequate"
    if total_precip < 10:
        precip_analysis = "drought_risk"
    elif total_precip > 50:
        precip_analysis = "flood_risk"
    
    # Crop recommendations
    crop_recommendations = []
    if current["temp"] > 20 and current["humidity"] > 60:
        crop_recommendations.extend(["tomatoes", "peppers", "cucumbers"])
    elif current["temp"] < 15:
        crop_recommendations.extend(["lettuce", "spinach", "kale"])
    
    # Risk assessment
    risks = []
    if temp_analysis == "stress":
        risks.append("heat_stress_on_crops")
    if precip_analysis == "drought_risk":
        risks.append("water_shortage")
    if precip_analysis == "flood_risk":
        risks.append("crop_damage")
    
    return {
        "temperature_analysis": temp_analysis,
        "precipitation_analysis": precip_analysis,
        "total_precipitation_forecast": total_precip,
        "crop_recommendations": crop_recommendations,
        "risks": risks,
        "irrigation_needed": precip_analysis == "drought_risk",
        "harvest_timing": "delay" if precip_analysis == "flood_risk" else "proceed"
    }

def analyze_logistics_impact(weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze weather impact on logistics and transportation"""
    current = weather_data["current"]
    forecast = weather_data["forecast"]
    
    # Transportation conditions
    road_conditions = "good"
    if current["condition"] in ["rainy", "stormy"]:
        road_conditions = "poor"
    elif current["temp"] < 0:
        road_conditions = "hazardous"
    
    # Delivery delays
    delay_risk = "low"
    if road_conditions == "poor":
        delay_risk = "medium"
    elif road_conditions == "hazardous":
        delay_risk = "high"
    
    # Route recommendations
    route_recommendations = []
    if current["wind_speed"] > 20:
        route_recommendations.append("avoid_high_bridges")
    if current["condition"] == "stormy":
        route_recommendations.append("use_alternative_routes")
    
    # Fuel efficiency
    fuel_efficiency = "normal"
    if current["temp"] < 0 or current["temp"] > 30:
        fuel_efficiency = "reduced"
    
    return {
        "road_conditions": road_conditions,
        "delay_risk": delay_risk,
        "route_recommendations": route_recommendations,
        "fuel_efficiency": fuel_efficiency,
        "delivery_adjustments": "delay" if delay_risk == "high" else "proceed",
        "safety_alerts": len(route_recommendations) > 0
    }

def generate_business_recommendations(business_type: str, impact_analysis: Dict[str, Any]) -> List[str]:
    """Generate business-specific recommendations"""
    recommendations = []
    
    if business_type == "retail":
        if impact_analysis.get("sales_forecast") == "high":
            recommendations.append("Increase inventory of weather-appropriate products")
            recommendations.append("Extend store hours to capitalize on good weather")
        elif impact_analysis.get("sales_forecast") == "low":
            recommendations.append("Focus on online sales and delivery")
            recommendations.append("Offer weather-related promotions")
        
        if impact_analysis.get("product_recommendations"):
            recommendations.append(f"Promote: {', '.join(impact_analysis['product_recommendations'][:3])}")
    
    elif business_type == "agriculture":
        if impact_analysis.get("irrigation_needed"):
            recommendations.append("Schedule irrigation systems")
        if impact_analysis.get("harvest_timing") == "delay":
            recommendations.append("Delay harvest until weather improves")
        if impact_analysis.get("risks"):
            recommendations.append(f"Monitor for: {', '.join(impact_analysis['risks'])}")
    
    elif business_type == "logistics":
        if impact_analysis.get("delay_risk") == "high":
            recommendations.append("Communicate delays to customers")
            recommendations.append("Consider alternative transportation methods")
        if impact_analysis.get("safety_alerts"):
            recommendations.append("Update driver safety protocols")
    
    if not recommendations:
        recommendations.append("Weather conditions are favorable for normal operations")
    
    return recommendations

def assess_risks(business_type: str, weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Assess weather-related risks for business"""
    current = weather_data["current"]
    forecast = weather_data["forecast"]
    
    risks = {
        "overall_risk": "low",
        "specific_risks": [],
        "mitigation_strategies": []
    }
    
    # Temperature risks
    if current["temp"] > 35:
        risks["specific_risks"].append("heat_stress")
        risks["mitigation_strategies"].append("implement_cooling_systems")
    elif current["temp"] < 0:
        risks["specific_risks"].append("freezing_conditions")
        risks["mitigation_strategies"].append("prepare_for_cold_weather")
    
    # Precipitation risks
    high_precip_days = sum(1 for day in forecast if day["precipitation"] > 10)
    if high_precip_days > 3:
        risks["specific_risks"].append("extended_rainfall")
        risks["mitigation_strategies"].append("prepare_flood_protection")
    
    # Wind risks
    if current["wind_speed"] > 25:
        risks["specific_risks"].append("high_winds")
        risks["mitigation_strategies"].append("secure_outdoor_equipment")
    
    # Determine overall risk level
    if len(risks["specific_risks"]) >= 3:
        risks["overall_risk"] = "high"
    elif len(risks["specific_risks"]) >= 1:
        risks["overall_risk"] = "medium"
    
    return risks

@router.post("/analyze", response_model=WeatherBusinessResponse)
async def analyze_weather_business_impact(request: WeatherBusinessRequest):
    """
    Analyze weather impact on business operations and provide recommendations.
    
    - **location**: Location for weather analysis
    - **business_type**: Type of business (retail, agriculture, logistics, tourism, construction)
    - **analysis_type**: Type of analysis to perform
    - **forecast_days**: Number of days to forecast
    """
    try:
        # Get weather data
        weather_data = get_weather_data(request.location)
        
        # Analyze business impact based on type
        if request.business_type == "retail":
            impact_analysis = analyze_retail_impact(weather_data)
        elif request.business_type == "agriculture":
            impact_analysis = analyze_agriculture_impact(weather_data)
        elif request.business_type == "logistics":
            impact_analysis = analyze_logistics_impact(weather_data)
        else:
            impact_analysis = analyze_retail_impact(weather_data)  # Default
        
        # Generate recommendations
        recommendations = generate_business_recommendations(request.business_type, impact_analysis)
        
        # Assess risks
        risk_assessment = assess_risks(request.business_type, weather_data)
        
        # Forecast analysis
        forecast_analysis = {
            "forecast_days": request.forecast_days,
            "temperature_trend": "stable",
            "precipitation_trend": "stable",
            "business_outlook": "positive" if impact_analysis.get("sales_forecast") == "high" else "negative" if impact_analysis.get("sales_forecast") == "low" else "stable"
        }
        
        return WeatherBusinessResponse(
            location=request.location,
            business_type=request.business_type,
            current_weather=weather_data["current"],
            business_impact=impact_analysis,
            recommendations=recommendations,
            risk_assessment=risk_assessment,
            forecast_analysis=forecast_analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather business analysis failed: {str(e)}")

@router.get("/seasonal-analysis/{location}/{business_type}")
async def get_seasonal_analysis(location: str, business_type: str, season: str):
    """Get seasonal weather patterns and business impact analysis"""
    try:
        # Mock seasonal data
        seasonal_data = {
            "spring": {"avg_temp": 15, "avg_precip": 20, "business_impact": "moderate"},
            "summer": {"avg_temp": 25, "avg_precip": 10, "business_impact": "high"},
            "fall": {"avg_temp": 15, "avg_precip": 25, "business_impact": "moderate"},
            "winter": {"avg_temp": 5, "avg_precip": 30, "business_impact": "low"}
        }
        
        season_info = seasonal_data.get(season, seasonal_data["spring"])
        
        return {
            "location": location,
            "business_type": business_type,
            "season": season,
            "seasonal_data": season_info,
            "recommendations": [
                f"Prepare for {season} weather patterns",
                "Adjust inventory based on seasonal demand",
                "Update marketing strategies for seasonal trends"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seasonal analysis failed: {str(e)}")

@router.get("/weather-alerts/{location}")
async def get_weather_alerts(location: str):
    """Get current weather alerts for a location"""
    try:
        weather_data = get_weather_data(location)
        current = weather_data["current"]
        
        alerts = []
        
        if current["temp"] > 35:
            alerts.append({"type": "heat_warning", "severity": "high", "message": "Extreme heat conditions"})
        elif current["temp"] < 0:
            alerts.append({"type": "freeze_warning", "severity": "medium", "message": "Freezing conditions"})
        
        if current["condition"] == "stormy":
            alerts.append({"type": "storm_warning", "severity": "high", "message": "Severe weather conditions"})
        
        if current["wind_speed"] > 25:
            alerts.append({"type": "wind_warning", "severity": "medium", "message": "High wind conditions"})
        
        return {
            "location": location,
            "alerts": alerts,
            "alert_count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather alerts failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the weather business intelligence service"""
    return {"status": "healthy", "service": "weather_business_intelligence"} 