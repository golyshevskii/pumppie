#!/usr/bin/env python3
"""Market Data MCP Server for PumpPie agent."""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("pumppie-market-data-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available market data tools."""
    return [
        Tool(
            name="get_asset_price",
            description="Get current price and basic info for a cryptocurrency asset",
            inputSchema={
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "Asset symbol (e.g., BTC, ETH, ADA)"}},
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_price_history",
            description="Get historical price data for technical analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Asset symbol"},
                    "days": {"type": "integer", "description": "Number of days of history to fetch", "default": 30},
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="calculate_technical_indicators",
            description="Calculate technical indicators (RSI, SMA, EMA, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Asset symbol"},
                    "indicators": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of indicators to calculate",
                        "default": ["rsi", "sma_20", "ema_12", "volatility"],
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_market_sentiment",
            description="Get market sentiment indicators and fear/greed index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Asset symbol (optional, for asset-specific sentiment)",
                        "default": "BTC",
                    }
                },
                "required": [],
            },
        ),
        Tool(
            name="analyze_volatility",
            description="Analyze price volatility and risk metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Asset symbol"},
                    "period_days": {"type": "integer", "description": "Analysis period in days", "default": 30},
                },
                "required": ["symbol"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Call a market data tool with given arguments."""
    if name == "get_asset_price":
        symbol = arguments.get("symbol", "").upper()

        # Mock data - in production, integrate with real API (CoinGecko, CoinMarketCap, etc.)
        mock_prices = {
            "BTC": {"price": 43250.50, "change_24h": 2.3, "volume_24h": 25000000000, "market_cap": 850000000000},
            "ETH": {"price": 2580.75, "change_24h": -1.2, "volume_24h": 15000000000, "market_cap": 310000000000},
            "ADA": {"price": 0.45, "change_24h": 5.1, "volume_24h": 800000000, "market_cap": 16000000000},
            "SOL": {"price": 105.20, "change_24h": 3.8, "volume_24h": 2500000000, "market_cap": 47000000000},
        }

        data = mock_prices.get(
            symbol, {"price": 1.0, "change_24h": 0.0, "volume_24h": 1000000, "market_cap": 1000000000}
        )

        result = {
            "symbol": symbol,
            "current_price": data["price"],
            "price_change_24h": data["change_24h"],
            "volume_24h": data["volume_24h"],
            "market_cap": data["market_cap"],
            "timestamp": "2024-01-15T12:00:00Z",
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_price_history":
        symbol = arguments.get("symbol", "").upper()
        days = arguments.get("days", 30)

        # Mock historical data
        import random

        base_price = 43250.50 if symbol == "BTC" else 2580.75

        history = []
        current_price = base_price

        for i in range(days):
            # Simulate price movement
            change = random.uniform(-0.05, 0.05)  # ±5% daily change
            current_price *= 1 + change

            history.append(
                {
                    "date": f"2024-01-{15 - days + i:02d}",
                    "price": round(current_price, 2),
                    "volume": random.randint(1000000, 50000000),
                }
            )

        result = {"symbol": symbol, "period_days": days, "price_history": history}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calculate_technical_indicators":
        symbol = arguments.get("symbol", "").upper()
        indicators = arguments.get("indicators", ["rsi", "sma_20", "ema_12", "volatility"])

        # Mock technical indicators
        mock_indicators = {
            "rsi": {"value": 65.2, "signal": "neutral", "description": "RSI indicates neutral momentum"},
            "sma_20": {
                "value": 43100.0,
                "signal": "bullish",
                "description": "Price above 20-day SMA indicates uptrend",
            },
            "ema_12": {
                "value": 43180.0,
                "signal": "bullish",
                "description": "Price above 12-day EMA confirms bullish momentum",
            },
            "volatility": {"value": 4.2, "signal": "moderate", "description": "Volatility is at moderate levels"},
            "macd": {"value": 125.5, "signal": "bullish", "description": "MACD shows bullish divergence"},
            "bollinger_bands": {
                "upper": 45000.0,
                "middle": 43000.0,
                "lower": 41000.0,
                "signal": "neutral",
                "description": "Price within normal Bollinger Bands range",
            },
        }

        result = {
            "symbol": symbol,
            "indicators": {
                indicator: mock_indicators.get(indicator, {"value": 0, "signal": "unknown"}) for indicator in indicators
            },
            "analysis_timestamp": "2024-01-15T12:00:00Z",
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_market_sentiment":
        symbol = arguments.get("symbol", "BTC")

        # Mock sentiment data
        result = {
            "overall_sentiment": "neutral_bullish",
            "fear_greed_index": 68,
            "sentiment_score": 0.65,
            "social_mentions": 15420,
            "news_sentiment": "positive",
            "technical_sentiment": "bullish",
            "factors": [
                "Increased institutional interest",
                "Technical breakout patterns",
                "Positive regulatory developments",
                "Growing adoption metrics",
            ],
            "timestamp": "2024-01-15T12:00:00Z",
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "analyze_volatility":
        symbol = arguments.get("symbol", "").upper()
        period_days = arguments.get("period_days", 30)

        # Mock volatility analysis
        result = {
            "symbol": symbol,
            "period_days": period_days,
            "volatility_metrics": {
                "historical_volatility": 4.2,
                "volatility_percentile": 65,
                "volatility_trend": "decreasing",
                "risk_level": "moderate",
                "sharpe_ratio": 1.2,
                "max_drawdown": -15.3,
                "value_at_risk_95": -8.5,
            },
            "risk_assessment": {
                "suitable_for_dca": True,
                "risk_adjusted_allocation": 0.15,
                "recommended_position_size": "moderate",
                "warnings": ["High volatility periods may increase DCA efficiency"],
            },
            "timestamp": "2024-01-15T12:00:00Z",
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the Market Data MCP server."""
    logger.info("Starting PumpPie Market Data MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
