#!/usr/bin/env python3
"""Basic tests for PumpPie agent."""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import PumpPieAgent, MCPClient
from core.agent.config import AgentConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mcp_client():
    """Test basic MCP client functionality."""
    logger.info("Testing MCP client...")
    
    client = MCPClient()
    
    try:
        # Try to connect to test server
        await client.add_server(
            "test",
            "python", 
            ["-m", "core.agent.tools.test_server"]
        )
        
        # List tools
        tools = await client.list_tools("test")
        logger.info(f"Available tools: {[tool.get('name') for tool in tools]}")
        
        # Test echo tool
        result = await client.call_tool("test", "echo", {"message": "Hello MCP!"})
        logger.info(f"Echo result: {result}")
        
        # Test calculate tool
        result = await client.call_tool("test", "calculate", {"expression": "2 + 2"})
        logger.info(f"Calculate result: {result}")
        
        # Get server info
        info = await client.get_server_info("test")
        logger.info(f"Server info: {info}")
        
        logger.info("✅ MCP client test passed!")
        
    except Exception as e:
        logger.error(f"❌ MCP client test failed: {e}")
        
    finally:
        await client.close()


async def test_agent_basic():
    """Test basic agent functionality."""
    logger.info("Testing PumpPie agent...")
    
    try:
        # Create agent config
        config = AgentConfig.create_default(user_id=12345)
        logger.info(f"Created config for user {config.user_id}")
        
        # Create agent
        agent = PumpPieAgent(user_id=12345, config=config.to_dict())
        
        # Test initialization
        await agent.initialize()
        logger.info("Agent initialized")
        
        # Test health check
        health = await agent.health_check()
        logger.info(f"Agent health: {health}")
        
        # Test portfolio status
        portfolio = await agent.get_portfolio_status()
        logger.info(f"Portfolio status: {portfolio}")
        
        # Test message processing
        response = await agent.process_message("Hello agent!")
        logger.info(f"Agent response: {response}")
        
        # Test DCA strategy
        success = await agent.start_dca_strategy("BTC", 100.0, "weekly")
        logger.info(f"DCA strategy started: {success}")
        
        # Test market analysis
        analysis = await agent.get_market_analysis("BTC")
        logger.info(f"Market analysis: {analysis}")
        
        logger.info("✅ Agent basic test passed!")
        
    except Exception as e:
        logger.error(f"❌ Agent basic test failed: {e}")
        
    finally:
        await agent.close()


async def test_config():
    """Test agent configuration."""
    logger.info("Testing agent configuration...")
    
    try:
        # Create default config
        config = AgentConfig.create_default(user_id=67890)
        
        # Convert to dict and back
        config_dict = config.to_dict()
        config_restored = AgentConfig.from_dict(config_dict)
        
        assert config.user_id == config_restored.user_id
        assert config.language == config_restored.language
        assert len(config.mcp_servers) == len(config_restored.mcp_servers)
        
        logger.info("✅ Config test passed!")
        
    except Exception as e:
        logger.error(f"❌ Config test failed: {e}")


async def main():
    """Run all tests."""
    logger.info("🚀 Starting PumpPie agent tests...")
    
    await test_config()
    await test_mcp_client()
    await test_agent_basic()
    
    logger.info("🎉 All tests completed!")


if __name__ == "__main__":
    asyncio.run(main()) 