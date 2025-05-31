#!/usr/bin/env python3
"""Quick test of PumpPie agent."""

import asyncio
import sys
from decimal import Decimal

from core.agent import PumpPieAgent

async def main():
    """Test basic agent functionality."""
    print("🚀 Testing PumpPie Agent...")
    
    try:
        # Create agent
        agent = PumpPieAgent(user_id=12345, model="test")
        print("✅ Agent created successfully!")
        print(f"   User ID: {agent.user_id}")
        print(f"   Model: {agent.model}")
        
        # Test health check
        health = await agent.health_check()
        print("✅ Health check passed!")
        print(f"   Status: {health['status']}")
        print(f"   Agents: {health['agents_initialized']}")
        
        # Test message processing
        response = await agent.process_message("Hello, PumpPie!")
        print("✅ Message processing works!")
        print(f"   Response: {response}")
        
        # Test DCA strategy creation
        strategy = await agent.create_dca_strategy(
            asset="BTC",
            amount=Decimal("100"),
            interval="weekly",
            duration_months=12
        )
        print("✅ DCA strategy creation works!")
        print(f"   Strategy ID: {strategy.strategy_id}")
        print(f"   Risk: {strategy.risk_assessment}")
        
        # Test portfolio status
        portfolio = await agent.get_portfolio_status()
        print("✅ Portfolio status works!")
        print(f"   Total value: ${portfolio.total_value}")
        print(f"   P&L: {portfolio.total_pnl_percentage}%")
        
        # Test market analysis
        analysis = await agent.get_market_analysis("BTC")
        print("✅ Market analysis works!")
        print(f"   Trend: {analysis.trend_direction}")
        print(f"   Recommendation: {analysis.investment_recommendation}")
        
        print("\n🎉 All tests passed! PydanticAI agent is working correctly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 