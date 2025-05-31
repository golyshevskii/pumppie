#!/usr/bin/env python3
"""Check availability of official MCP servers."""

import asyncio
import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_npx_availability():
    """Check if npx is available."""
    try:
        result = subprocess.run(["npx", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ npx available: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"❌ npx failed: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("❌ npx not found. Please install Node.js and npm")
        return False
    except subprocess.TimeoutExpired:
        logger.error("❌ npx check timed out")
        return False


async def check_mcp_server(name: str, args: list, timeout: int = 30):
    """Check if MCP server is available and can start."""
    logger.info(f"🔍 Checking {name}...")
    
    try:
        # Try to install and run the server briefly
        cmd = ["npx", "-y"] + args + ["--help"]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        if result.returncode == 0:
            logger.info(f"✅ {name} available")
            return True
        else:
            logger.warning(f"⚠️ {name} - return code {result.returncode}")
            logger.debug(f"stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.warning(f"⏱️ {name} check timed out")
        return False
    except Exception as e:
        logger.error(f"❌ {name} error: {e}")
        return False


async def check_official_servers():
    """Check official MCP servers availability."""
    servers_to_check = [
        ("Memory Server", ["@modelcontextprotocol/server-memory"]),
        ("Fetch Server", ["@modelcontextprotocol/server-fetch"]),
        ("SQLite Server", ["@modelcontextprotocol/server-sqlite", "test.db"]),
        ("Filesystem Server", ["@modelcontextprotocol/server-filesystem", "."]),
    ]
    
    results = {}
    
    for name, args in servers_to_check:
        available = await check_mcp_server(name, args)
        results[name] = available
        
        if not available:
            logger.info(f"   To install: npx -y {' '.join(args[:1])}")
    
    return results


async def check_custom_servers():
    """Check our custom MCP servers."""
    logger.info("\n🔍 Checking custom servers...")
    
    # Check if our market data server can be imported
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from core.agent.tools.market_data_server import server
        logger.info("✅ Custom market data server available")
        return {"Market Data Server": True}
    except ImportError as e:
        logger.error(f"❌ Custom market data server import failed: {e}")
        return {"Market Data Server": False}


async def main():
    """Main check function."""
    logger.info("🚀 Checking MCP Servers Availability for PumpPie\n")
    
    # Check npx availability
    npx_available = await check_npx_availability()
    
    if not npx_available:
        logger.error("\n❌ Cannot proceed without npx. Please install Node.js and npm first.")
        sys.exit(1)
    
    logger.info("\n" + "="*50)
    logger.info("OFFICIAL MCP SERVERS")
    logger.info("="*50)
    
    # Check official servers
    official_results = await check_official_servers()
    
    logger.info("\n" + "="*50)
    logger.info("CUSTOM MCP SERVERS")
    logger.info("="*50)
    
    # Check custom servers
    custom_results = await check_custom_servers()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("SUMMARY")
    logger.info("="*50)
    
    all_available = True
    
    for name, available in {**official_results, **custom_results}.items():
        status = "✅ Available" if available else "❌ Not Available"
        logger.info(f"{name}: {status}")
        if not available:
            all_available = False
    
    if all_available:
        logger.info("\n🎉 All MCP servers are available! PumpPie agent ready to use production servers.")
    else:
        logger.warning("\n⚠️ Some servers unavailable. PumpPie will work in test mode.")
        logger.info("\nTo install missing servers:")
        logger.info("npm install -g @modelcontextprotocol/server-memory")
        logger.info("npm install -g @modelcontextprotocol/server-fetch")
        logger.info("npm install -g @modelcontextprotocol/server-sqlite")
        logger.info("npm install -g @modelcontextprotocol/server-filesystem")
    
    return all_available


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Check interrupted")
        sys.exit(1) 