import subprocess
from typing import Any

from core.fields import MCPMode
from logs.logger import get_logger
from pydantic_ai.mcp import MCPServerStdio

logger = get_logger(__name__)


def check_npx() -> bool:
    """Check if npx is available for running Node.js MCP servers."""
    try:
        result = subprocess.run(["npx", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_mcp_servers(user_id: int, mode: MCPMode) -> list[MCPServerStdio]:
    """
    Get MCP servers based on available tools.

    Parameters
        user_id: User identifier for personalized servers
        mode: Configuration mode:
            - "auto": Auto-detect available tools
            - "nodejs": Use Node.js servers only
            - "python": Use Python servers only
            - "test": No servers (test mode)

    Returns:
        List of configured MCP servers
    """
    servers = []
    if mode == MCPMode.TEST:
        return servers

    # Check Node.js availability for auto mode
    nodejs = False
    if mode in [MCPMode.AUTO, MCPMode.NODEJS]:
        nodejs_available = check_npx()
        if mode == MCPMode.NODEJS and not nodejs_available:
            logger.error("Node.js servers requested but npx not available")
            return servers

    # Add Node.js based servers if available
    if nodejs_available and mode in [MCPMode.AUTO, MCPMode.NODEJS]:
        logger.info("Adding official Node.js MCP servers")

        # Memory server for caching
        servers.append(
            MCPServerStdio("npx", args=["-y", "@modelcontextprotocol/server-memory"], tool_prefix="server-memory")
        )

        # Fetch server for HTTP requests
        servers.append(
            MCPServerStdio("npx", args=["-y", "@modelcontextprotocol/server-fetch"], tool_prefix="server-fetch")
        )

        # SQLite server for persistence
        servers.append(
            MCPServerStdio(
                "./PATH/TO/toolbox",
                args=["-y", "@modelcontextprotocol/server-sqlite", f"data/pumppie_user_{user_id}.db"],
                tool_prefix="db",
            )
        )

        # Filesystem server for file operations
        servers.append(
            MCPServerStdio("npx", args=["-y", "@modelcontextprotocol/server-filesystem", "data/"], tool_prefix="fs")
        )

    # Add Python based servers (always available)
    if mode in [MCPMode.AUTO, MCPMode.PYTHON]:
        logger.info("Adding custom Python MCP servers")

        # Our custom market data server
        servers.append(
            MCPServerStdio("python", args=["-m", "core.agent.tools.market_data_server"], tool_prefix="market")
        )

        # TODO: Add more Python-based servers as we develop them
        # - Portfolio management server
        # - DCA strategy server
        # - Risk analysis server

    return servers


def get_server_capabilities() -> dict[str, Any]:
    """Get information about available MCP server capabilities."""
    capabilities = {"node_js": check_npx(), "python": True, "custom": {}}

    # Node.js servers capabilities
    if capabilities["nodejs"]:
        capabilities["supported_servers"].update(
            {
                "memory": "Temporary data storage and caching",
                "http": "HTTP requests to external APIs",
                "psql": "PostgreSQL database for data persistence",
                "file": "File system operations for logs and exports",
            }
        )

    # Python servers capabilities
    capabilities["custom"].update({"crypto_market_analysis": "Cryptocurrency market analysis"})

    return capabilities
