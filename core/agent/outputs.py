"""Output models for PumpPie AI Agent responses."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level enumeration."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class InvestmentRecommendation(str, Enum):
    """Investment recommendation enumeration."""

    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    AVOID = "avoid"


class TrendDirection(str, Enum):
    """Market trend direction enumeration."""

    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"


class AgentResponseOutput(BaseModel):
    """General agent conversation response."""

    response: str = Field(description="Agent response to user message")
    confidence: float = Field(description="Confidence level (0.0-1.0)", ge=0.0, le=1.0, default=0.8)
    suggested_actions: list[str] = Field(description="Suggested follow-up actions", default_factory=list)
    warning_flags: list[str] = Field(description="Any warnings or important notes", default_factory=list)


class DCAStrategyOutput(BaseModel):
    """DCA strategy creation and analysis output."""

    strategy_id: str = Field(description="Unique strategy identifier")
    asset: str = Field(description="Target asset symbol")
    amount_per_interval: Decimal = Field(description="Investment amount per interval")
    interval: str = Field(description="Investment frequency (daily, weekly, monthly)")
    duration_months: int = Field(description="Strategy duration in months")

    # Market analysis
    current_price: Decimal = Field(description="Current asset price")
    risk_assessment: RiskLevel = Field(description="Overall risk level")
    recommendation: InvestmentRecommendation = Field(description="Investment recommendation")

    # Strategy details
    total_investment: Decimal = Field(description="Total planned investment")
    expected_purchases: int = Field(description="Number of expected purchases")
    entry_conditions: list[str] = Field(description="Conditions for starting strategy")
    exit_conditions: list[str] = Field(description="Conditions for stopping strategy")

    # Risk management
    stop_loss_threshold: Decimal | None = Field(description="Stop loss percentage", default=None)
    take_profit_threshold: Decimal | None = Field(description="Take profit percentage", default=None)

    explanation: str = Field(description="Detailed explanation of the strategy")
    warnings: list[str] = Field(description="Important warnings and considerations", default_factory=list)


class PortfolioPosition(BaseModel):
    """Individual portfolio position."""

    asset: str = Field(description="Asset symbol")
    quantity: Decimal = Field(description="Quantity held")
    average_price: Decimal = Field(description="Average purchase price")
    current_price: Decimal = Field(description="Current market price")
    current_value: Decimal = Field(description="Current position value")
    unrealized_pnl: Decimal = Field(description="Unrealized profit/loss")
    unrealized_pnl_percentage: Decimal = Field(description="Unrealized P&L percentage")


class DCAStrategyStatus(BaseModel):
    """DCA strategy status."""

    strategy_id: str = Field(description="Strategy identifier")
    asset: str = Field(description="Target asset")
    status: str = Field(description="Strategy status (active, paused, completed)")
    total_invested: Decimal = Field(description="Total amount invested so far")
    total_quantity: Decimal = Field(description="Total asset quantity acquired")
    average_price: Decimal = Field(description="Average purchase price")
    next_purchase_date: datetime | None = Field(description="Next scheduled purchase")
    performance: Decimal = Field(description="Strategy performance percentage")


class PortfolioStatusOutput(BaseModel):
    """Portfolio status and analysis output."""

    # Overview
    total_value: Decimal = Field(description="Total portfolio value")
    total_invested: Decimal = Field(description="Total amount invested")
    total_pnl: Decimal = Field(description="Total profit/loss")
    total_pnl_percentage: Decimal = Field(description="Total P&L percentage")

    # Positions
    positions: list[PortfolioPosition] = Field(description="Individual asset positions")
    position_count: int = Field(description="Number of different assets held")

    # DCA Strategies
    active_strategies: list[DCAStrategyStatus] = Field(description="Active DCA strategies")
    strategy_count: int = Field(description="Number of active strategies")

    # Risk metrics
    portfolio_risk: RiskLevel = Field(description="Overall portfolio risk level")
    diversification_score: float = Field(description="Portfolio diversification score (0.0-1.0)", ge=0.0, le=1.0)
    largest_position_percentage: Decimal = Field(description="Percentage of largest position")

    # Recommendations
    recommendations: list[str] = Field(description="Portfolio optimization recommendations")
    warnings: list[str] = Field(description="Risk warnings and alerts", default_factory=list)

    analysis_summary: str = Field(description="Comprehensive portfolio analysis summary")


class TechnicalIndicator(BaseModel):
    """Technical indicator data."""

    name: str = Field(description="Indicator name")
    value: Decimal = Field(description="Current indicator value")
    signal: str = Field(description="Signal interpretation (bullish/bearish/neutral)")
    description: str = Field(description="Human-readable description")


class PriceLevel(BaseModel):
    """Support or resistance price level."""

    level: Decimal = Field(description="Price level")
    type: str = Field(description="Level type (support/resistance)")
    strength: str = Field(description="Level strength (weak/moderate/strong)")
    distance_percentage: Decimal = Field(description="Distance from current price as percentage")


class MarketAnalysisOutput(BaseModel):
    """Market analysis output."""

    # Basic info
    asset: str = Field(description="Asset symbol")
    current_price: Decimal = Field(description="Current market price")
    price_change_24h: Decimal = Field(description="24-hour price change percentage")
    volume_24h: Decimal = Field(description="24-hour trading volume")
    market_cap: Decimal | None = Field(description="Market capitalization", default=None)

    # Trend analysis
    trend_direction: TrendDirection = Field(description="Overall market trend")
    trend_strength: float = Field(description="Trend strength (0.0-1.0)", ge=0.0, le=1.0)
    volatility: Decimal = Field(description="Price volatility percentage")

    # Technical analysis
    technical_indicators: list[TechnicalIndicator] = Field(description="Technical indicators analysis")
    support_levels: list[PriceLevel] = Field(description="Support price levels")
    resistance_levels: list[PriceLevel] = Field(description="Resistance price levels")

    # Investment analysis
    investment_recommendation: InvestmentRecommendation = Field(description="Investment recommendation")
    dca_suitability: RiskLevel = Field(description="Suitability for DCA investment")
    optimal_entry_range: dict[str, Decimal] = Field(description="Optimal entry price range")

    # Risk assessment
    risk_factors: list[str] = Field(description="Identified risk factors")
    opportunity_factors: list[str] = Field(description="Identified opportunities")

    # Timing
    best_entry_timing: str = Field(description="Best timing for entry")
    market_sentiment: str = Field(description="Overall market sentiment")

    detailed_analysis: str = Field(description="Comprehensive market analysis summary")
    confidence_score: float = Field(description="Analysis confidence (0.0-1.0)", ge=0.0, le=1.0, default=0.8)
