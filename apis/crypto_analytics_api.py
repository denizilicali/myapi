from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests
import json
from datetime import datetime, timedelta
import statistics

router = APIRouter()

class PortfolioAsset(BaseModel):
    symbol: str
    quantity: float
    purchase_price: float
    purchase_date: str

class PortfolioRequest(BaseModel):
    assets: List[PortfolioAsset]
    base_currency: str = "USD"

class PortfolioAnalytics(BaseModel):
    total_value: float
    total_invested: float
    total_profit_loss: float
    profit_loss_percentage: float
    best_performer: Dict[str, Any]
    worst_performer: Dict[str, Any]
    portfolio_metrics: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    recommendations: List[str]

# Mock crypto price data (in real implementation, you'd use CoinGecko, CoinMarketCap, etc.)
MOCK_PRICES = {
    "BTC": 45000,
    "ETH": 3200,
    "ADA": 1.20,
    "DOT": 25.50,
    "LINK": 18.75,
    "UNI": 12.30,
    "SOL": 95.00,
    "MATIC": 1.85,
    "AVAX": 65.20,
    "ATOM": 28.90
}

def get_current_price(symbol: str) -> float:
    """Get current price for a cryptocurrency (mock implementation)"""
    # In real implementation, this would call CoinGecko API
    return MOCK_PRICES.get(symbol.upper(), 0.0)

def calculate_portfolio_metrics(assets: List[PortfolioAsset]) -> Dict[str, Any]:
    """Calculate comprehensive portfolio metrics"""
    portfolio_data = []
    total_invested = 0
    total_current_value = 0
    
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        current_value = asset.quantity * current_price
        invested_value = asset.quantity * asset.purchase_price
        profit_loss = current_value - invested_value
        profit_loss_pct = (profit_loss / invested_value * 100) if invested_value > 0 else 0
        
        asset_data = {
            "symbol": asset.symbol,
            "quantity": asset.quantity,
            "purchase_price": asset.purchase_price,
            "current_price": current_price,
            "current_value": current_value,
            "invested_value": invested_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_pct,
            "weight": 0  # Will be calculated later
        }
        
        portfolio_data.append(asset_data)
        total_invested += invested_value
        total_current_value += current_value
    
    # Calculate weights
    for asset in portfolio_data:
        asset["weight"] = (asset["current_value"] / total_current_value * 100) if total_current_value > 0 else 0
    
    return {
        "portfolio_data": portfolio_data,
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_profit_loss": total_current_value - total_invested,
        "total_profit_loss_percentage": ((total_current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
    }

def analyze_risk(portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze portfolio risk metrics"""
    if not portfolio_data:
        return {"risk_level": "unknown", "diversification_score": 0, "concentration_risk": "high"}
    
    # Calculate diversification score
    weights = [asset["weight"] for asset in portfolio_data]
    max_weight = max(weights) if weights else 0
    
    # Herfindahl-Hirschman Index for concentration
    hhi = sum(w**2 for w in weights)
    
    # Risk assessment
    if hhi > 0.25:  # Highly concentrated
        risk_level = "high"
        concentration_risk = "high"
    elif hhi > 0.15:  # Moderately concentrated
        risk_level = "medium"
        concentration_risk = "medium"
    else:  # Well diversified
        risk_level = "low"
        concentration_risk = "low"
    
    # Calculate volatility (mock - in real implementation, use historical data)
    profit_loss_pcts = [asset["profit_loss_percentage"] for asset in portfolio_data]
    volatility = statistics.stdev(profit_loss_pcts) if len(profit_loss_pcts) > 1 else 0
    
    return {
        "risk_level": risk_level,
        "diversification_score": max(0, 100 - hhi * 100),
        "concentration_risk": concentration_risk,
        "herfindahl_index": hhi,
        "max_position_weight": max_weight,
        "volatility": volatility,
        "asset_count": len(portfolio_data)
    }

def generate_recommendations(portfolio_data: List[Dict[str, Any]], risk_analysis: Dict[str, Any]) -> List[str]:
    """Generate investment recommendations"""
    recommendations = []
    
    # Diversification recommendations
    if risk_analysis["concentration_risk"] == "high":
        recommendations.append("Consider diversifying your portfolio to reduce concentration risk")
    
    if len(portfolio_data) < 5:
        recommendations.append("Consider adding more assets to improve diversification")
    
    # Performance-based recommendations
    underperformers = [asset for asset in portfolio_data if asset["profit_loss_percentage"] < -10]
    if underperformers:
        recommendations.append(f"Review {len(underperformers)} underperforming assets")
    
    # Rebalancing recommendations
    if risk_analysis["max_position_weight"] > 50:
        recommendations.append("Consider rebalancing to reduce exposure to your largest position")
    
    if not recommendations:
        recommendations.append("Your portfolio appears well-balanced. Continue monitoring market conditions.")
    
    return recommendations

@router.post("/analyze-portfolio", response_model=PortfolioAnalytics)
async def analyze_portfolio(request: PortfolioRequest):
    """
    Analyze cryptocurrency portfolio performance and provide insights.
    
    - **assets**: List of portfolio assets with quantities and purchase details
    - **base_currency**: Base currency for calculations (default: USD)
    """
    try:
        # Calculate portfolio metrics
        metrics = calculate_portfolio_metrics(request.assets)
        
        # Find best and worst performers
        portfolio_data = metrics["portfolio_data"]
        if portfolio_data:
            best_performer = max(portfolio_data, key=lambda x: x["profit_loss_percentage"])
            worst_performer = min(portfolio_data, key=lambda x: x["profit_loss_percentage"])
        else:
            best_performer = {}
            worst_performer = {}
        
        # Analyze risk
        risk_analysis = analyze_risk(portfolio_data)
        
        # Generate recommendations
        recommendations = generate_recommendations(portfolio_data, risk_analysis)
        
        return PortfolioAnalytics(
            total_value=metrics["total_current_value"],
            total_invested=metrics["total_invested"],
            total_profit_loss=metrics["total_profit_loss"],
            profit_loss_percentage=metrics["total_profit_loss_percentage"],
            best_performer=best_performer,
            worst_performer=worst_performer,
            portfolio_metrics=metrics,
            risk_analysis=risk_analysis,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portfolio analysis failed: {str(e)}")

@router.get("/market-overview")
async def get_market_overview():
    """Get overview of cryptocurrency market conditions"""
    try:
        # Mock market data (in real implementation, fetch from API)
        market_data = {
            "total_market_cap": 2500000000000,  # $2.5T
            "bitcoin_dominance": 42.5,
            "market_sentiment": "neutral",
            "top_gainers": [
                {"symbol": "SOL", "change_24h": 8.5},
                {"symbol": "AVAX", "change_24h": 6.2},
                {"symbol": "MATIC", "change_24h": 4.8}
            ],
            "top_losers": [
                {"symbol": "LINK", "change_24h": -3.2},
                {"symbol": "UNI", "change_24h": -2.1},
                {"symbol": "DOT", "change_24h": -1.8}
            ],
            "market_fear_greed_index": 65,  # 0-100 scale
            "last_updated": datetime.now().isoformat()
        }
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market overview failed: {str(e)}")

@router.get("/price/{symbol}")
async def get_crypto_price(symbol: str):
    """Get current price for a specific cryptocurrency"""
    try:
        price = get_current_price(symbol)
        if price == 0:
            raise HTTPException(status_code=404, detail=f"Price not found for {symbol}")
        
        return {
            "symbol": symbol.upper(),
            "price_usd": price,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price fetch failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the crypto analytics service"""
    return {"status": "healthy", "service": "crypto_analytics"} 