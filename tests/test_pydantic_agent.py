#!/usr/bin/env python3
"""Tests for PumpPie PydanticAI agent."""

import asyncio
import pytest
import logging
import sys
from decimal import Decimal
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import PumpPieAgent, AgentDependencies
from core.agent.outputs import (
    DCAStrategyOutput, PortfolioStatusOutput, MarketAnalysisOutput,
    RiskLevel, InvestmentRecommendation, TrendDirection
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
async def test_agent():
    """Create a test agent instance."""
    # Use test model to avoid API calls
    agent = PumpPieAgent(
        user_id=12345, 
        model="test",  # PydanticAI test model
        config={"test_mode": True}
    )
    return agent


@pytest.fixture
def test_dependencies():
    """Create test dependencies."""
    return AgentDependencies(user_id=12345)


@pytest.mark.asyncio
async def test_agent_initialization(test_agent):
    """Test basic agent initialization."""
    assert test_agent.user_id == 12345
    assert test_agent.config == {"test_mode": True}
    assert len(test_agent.mcp_servers) == 3  # market, portfolio, dca servers
    
    # Test that agents are properly initialized
    assert test_agent.conversation_agent is not None
    assert test_agent.dca_agent is not None
    assert test_agent.portfolio_agent is not None
    assert test_agent.market_agent is not None


@pytest.mark.asyncio
async def test_agent_dependencies(test_dependencies):
    """Test agent dependencies functionality."""
    deps = test_dependencies
    
    # Test user config retrieval
    config = await deps.get_user_config(12345)
    assert config is not None
    assert "preferences" in config
    assert "risk_tolerance" in config
    assert config["risk_tolerance"] == "moderate"
    
    # Test portfolio retrieval
    portfolio = await deps.get_user_portfolio(12345)
    assert portfolio is not None
    assert "total_value" in portfolio
    assert "positions" in portfolio
    
    # Test market data retrieval
    market_data = await deps.get_market_data("BTC")
    assert market_data is not None
    assert "symbol" in market_data
    assert "price" in market_data
    assert market_data["symbol"] == "BTC"


@pytest.mark.asyncio
async def test_health_check(test_agent):
    """Test agent health check."""
    health_status = await test_agent.health_check()
    
    assert health_status is not None
    assert health_status["user_id"] == 12345
    assert "agents_initialized" in health_status
    assert "mcp_servers_count" in health_status
    assert "status" in health_status
    
    # In test mode, this should be healthy
    logger.info(f"Health status: {health_status}")


@pytest.mark.asyncio
async def test_process_message_basic():
    """Test basic message processing."""
    # Skip this test as it requires actual model API
    pytest.skip("Requires LLM API configuration")


@pytest.mark.asyncio
async def test_dca_strategy_output_validation():
    """Test DCA strategy output validation."""
    # Test that our Pydantic models work correctly
    strategy_data = {
        "strategy_id": "dca_12345_BTC",
        "asset": "BTC",
        "amount_per_interval": Decimal("100.00"),
        "interval": "weekly",
        "duration_months": 12,
        "current_price": Decimal("43250.50"),
        "risk_assessment": RiskLevel.MODERATE,
        "recommendation": InvestmentRecommendation.BUY,
        "total_investment": Decimal("5200.00"),
        "expected_purchases": 52,
        "entry_conditions": ["Market RSI below 70", "Price above 20-day SMA"],
        "exit_conditions": ["Take profit at 100% gain", "Stop loss at 20% loss"],
        "explanation": "Well-balanced DCA strategy for Bitcoin accumulation",
        "warnings": ["Cryptocurrency investments are highly volatile"]
    }
    
    # This should not raise validation errors
    strategy = DCAStrategyOutput(**strategy_data)
    assert strategy.asset == "BTC"
    assert strategy.amount_per_interval == Decimal("100.00")
    assert strategy.risk_assessment == RiskLevel.MODERATE


@pytest.mark.asyncio
async def test_portfolio_status_output_validation():
    """Test portfolio status output validation."""
    portfolio_data = {
        "total_value": Decimal("10000.00"),
        "total_invested": Decimal("8500.00"),
        "total_pnl": Decimal("1500.00"),
        "total_pnl_percentage": Decimal("17.65"),
        "positions": [],
        "position_count": 0,
        "active_strategies": [],
        "strategy_count": 0,
        "portfolio_risk": RiskLevel.MODERATE,
        "diversification_score": 0.65,
        "largest_position_percentage": Decimal("0.00"),
        "recommendations": ["Consider diversifying into additional assets"],
        "warnings": [],
        "analysis_summary": "Portfolio showing positive performance with room for diversification"
    }
    
    # This should not raise validation errors
    portfolio = PortfolioStatusOutput(**portfolio_data)
    assert portfolio.total_value == Decimal("10000.00")
    assert portfolio.portfolio_risk == RiskLevel.MODERATE


@pytest.mark.asyncio
async def test_market_analysis_output_validation():
    """Test market analysis output validation."""
    analysis_data = {
        "asset": "BTC",
        "current_price": Decimal("43250.50"),
        "price_change_24h": Decimal("2.3"),
        "volume_24h": Decimal("25000000000"),
        "market_cap": Decimal("850000000000"),
        "trend_direction": TrendDirection.BULLISH,
        "trend_strength": 0.75,
        "volatility": Decimal("4.2"),
        "technical_indicators": [],
        "support_levels": [],
        "resistance_levels": [],
        "investment_recommendation": InvestmentRecommendation.BUY,
        "dca_suitability": RiskLevel.MODERATE,
        "optimal_entry_range": {"min": Decimal("42000"), "max": Decimal("44000")},
        "risk_factors": ["High volatility", "Regulatory uncertainty"],
        "opportunity_factors": ["Growing institutional adoption", "Technical breakout"],
        "best_entry_timing": "Current levels are favorable for DCA initiation",
        "market_sentiment": "Cautiously optimistic",
        "detailed_analysis": "Bitcoin showing strong technical indicators with moderate risk profile",
        "confidence_score": 0.8
    }
    
    # This should not raise validation errors
    analysis = MarketAnalysisOutput(**analysis_data)
    assert analysis.asset == "BTC"
    assert analysis.trend_direction == TrendDirection.BULLISH
    assert analysis.investment_recommendation == InvestmentRecommendation.BUY


@pytest.mark.asyncio
async def test_mcp_tool_integration():
    """Test MCP tool integration setup."""
    agent = PumpPieAgent(user_id=12345, model="test")
    
    # Verify MCP servers are configured correctly
    assert len(agent.mcp_servers) == 3
    
    server_names = []
    for server in agent.mcp_servers:
        # MCPServerStdio should have args attribute
        if hasattr(server, 'args') and server.args:
            server_names.append(server.args[-1].split('.')[-1])
    
    # Check that we have the expected server types
    expected_servers = ["market_data_server", "portfolio_server", "dca_server"]
    for expected in expected_servers:
        assert any(expected in name for name in server_names), f"Missing {expected}"


@pytest.mark.asyncio 
async def test_agent_specialization():
    """Test that we have specialized agents for different tasks."""
    agent = PumpPieAgent(user_id=12345, model="test")
    
    # Each agent should have different output types
    assert agent.conversation_agent._output_type is not None
    assert agent.dca_agent._output_type is not None  
    assert agent.portfolio_agent._output_type is not None
    assert agent.market_agent._output_type is not None
    
    # Agents should have different system prompts
    conv_prompt = agent.conversation_agent._system_prompt
    dca_prompt = agent.dca_agent._system_prompt
    
    assert conv_prompt != dca_prompt
    assert "PumpPie" in conv_prompt
    assert "DCA strategy specialist" in dca_prompt


async def main():
    """Run all tests."""
    logger.info("🚀 Starting PumpPie PydanticAI agent tests...")
    
    # Create test instances
    agent = PumpPieAgent(user_id=12345, model="test")
    deps = AgentDependencies(user_id=12345)
    
    try:
        # Run basic tests
        await test_agent_initialization(agent)
        logger.info("✅ Agent initialization test passed!")
        
        await test_agent_dependencies(deps)
        logger.info("✅ Agent dependencies test passed!")
        
        await test_health_check(agent)
        logger.info("✅ Health check test passed!")
        
        await test_dca_strategy_output_validation()
        logger.info("✅ DCA strategy output validation test passed!")
        
        await test_portfolio_status_output_validation()
        logger.info("✅ Portfolio status output validation test passed!")
        
        await test_market_analysis_output_validation()
        logger.info("✅ Market analysis output validation test passed!")
        
        await test_mcp_tool_integration()
        logger.info("✅ MCP tool integration test passed!")
        
        await test_agent_specialization()
        logger.info("✅ Agent specialization test passed!")
        
        logger.info("🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 