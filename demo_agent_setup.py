#!/usr/bin/env python3
"""Demo of PumpPie agent setup with different MCP configurations."""

import asyncio
import json
from core.agent import PumpPieAgent
from core.agent.mcp_config import get_server_capabilities, get_recommended_setup

async def demo_agent_configurations():
    """Demo different agent configuration modes."""
    print("🚀 PumpPie Agent Configuration Demo")
    print("=" * 50)
    
    # Show current system capabilities
    capabilities = get_server_capabilities()
    print("\n📊 System Capabilities:")
    print(f"   Node.js available: {capabilities['nodejs_available']}")
    print(f"   Python available: {capabilities['python_available']}")
    print(f"   Supported servers: {list(capabilities['supported_servers'].keys())}")
    
    # Show recommended setup
    recommended = get_recommended_setup()
    print(f"\n💡 Recommended Setup:")
    print(f"   Mode: {recommended['mode']}")
    print(f"   Description: {recommended['description']}")
    print(f"   Features: {', '.join(recommended['features'])}")
    if 'limitations' in recommended:
        print(f"   Limitations: {', '.join(recommended['limitations'])}")
    
    print("\n" + "=" * 50)
    print("TESTING DIFFERENT CONFIGURATIONS")
    print("=" * 50)
    
    # Test different modes
    modes_to_test = ["test", "python", "auto"]
    
    for mode in modes_to_test:
        print(f"\n🔧 Testing mode: {mode}")
        print("-" * 30)
        
        try:
            agent = PumpPieAgent(user_id=12345, model="test", mcp_mode=mode)
            setup_info = agent.get_setup_info()
            
            print(f"   MCP Mode: {setup_info['mcp_mode']}")
            print(f"   Active servers: {setup_info['active_servers']}")
            print(f"   Available capabilities: {list(setup_info['server_capabilities']['supported_servers'].keys())}")
            
            if setup_info['active_servers'] > 0:
                print("   Server list:")
                for server in setup_info['server_list']:
                    print(f"     - {server['prefix']}: {server['command']}")
            
            # Test basic functionality
            health = await agent.health_check()
            print(f"   Health status: {health['status']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("PRODUCTION USAGE EXAMPLES")
    print("=" * 50)
    
    print("\n📝 Example 1: Test mode (development)")
    print("```python")
    print("agent = PumpPieAgent(user_id=123, model='test', mcp_mode='test')")
    print("# No MCP servers, uses mock data")
    print("```")
    
    print("\n📝 Example 2: Python-only mode (limited)")
    print("```python")
    print("agent = PumpPieAgent(user_id=123, model='openai:gpt-4o', mcp_mode='python')")
    print("# Only custom Python MCP servers (market data)")
    print("```")
    
    if capabilities['nodejs_available']:
        print("\n📝 Example 3: Full mode (recommended)")
        print("```python")
        print("agent = PumpPieAgent(user_id=123, model='openai:gpt-4o', mcp_mode='auto')")
        print("# All available servers: memory, fetch, db, fs, market")
        print("```")
    else:
        print("\n📝 Example 3: Full mode setup")
        print("To enable full functionality:")
        print("1. Install Node.js: https://nodejs.org/")
        print("2. Install MCP servers: make mcp.install-official")
        print("3. Use auto mode: mcp_mode='auto'")
    
    print("\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    
    if not capabilities['nodejs_available']:
        print("\n⚠️  Limited functionality detected!")
        print("To unlock full PumpPie capabilities:")
        print("1. Install Node.js and npm")
        print("2. Run: make mcp.install-official")
        print("3. Test: make mcp.check")
        print("\nWithout Node.js, you'll have:")
        print("✅ Market data analysis")
        print("❌ Data persistence")
        print("❌ External API integration")
        print("❌ File exports")
    else:
        print("\n🎉 Full setup available!")
        print("You can use all PumpPie features including:")
        print("✅ Market data analysis")
        print("✅ Data persistence with SQLite")
        print("✅ External API integration")
        print("✅ File exports and logging")
        print("✅ Memory caching for performance")

if __name__ == "__main__":
    asyncio.run(demo_agent_configurations()) 