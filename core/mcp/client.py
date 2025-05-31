"""MCP (Model Context Protocol) client for PumpPie agent."""

import logging
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPClient:
    """MCP client for communicating with MCP servers."""

    def __init__(self) -> None:
        """Initialize MCP client."""
        self.sessions: dict[str, ClientSession] = {}
        self.servers: dict[str, StdioServerParameters] = {}

    async def add_server(self, name: str, command: str, args: list[str] | None = None) -> None:
        """
        Add and connect to an MCP server.

        Args:
            name: Server name identifier
            command: Command to run the server
            args: Optional command arguments
        """
        if args is None:
            args = []

        server_params = StdioServerParameters(command=command, args=args)

        self.servers[name] = server_params

        try:
            # Create session and connect
            session = await stdio_client(server_params)
            self.sessions[name] = session

            # Initialize the session
            await session.initialize()

            logger.info(f"Successfully connected to MCP server: {name}")

        except Exception as e:
            logger.error(f"Failed to connect to MCP server {name}: {e}")
            raise

    async def list_tools(self, server_name: str) -> list[dict[str, Any]]:
        """
        List available tools from a specific server.

        Args:
            server_name: Name of the server to query

        Returns:
            List of available tools
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")

        session = self.sessions[server_name]

        try:
            response = await session.list_tools()
            return response.tools
        except Exception as e:
            logger.error(f"Failed to list tools from {server_name}: {e}")
            raise

    async def call_tool(
        self, server_name: str, tool_name: str, arguments: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Call a tool on a specific server.

        Args:
            server_name: Name of the server
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")

        if arguments is None:
            arguments = {}

        session = self.sessions[server_name]

        try:
            response = await session.call_tool(tool_name, arguments)
            return response.content
        except Exception as e:
            logger.error(f"Failed to call tool {tool_name} on {server_name}: {e}")
            raise

    async def close(self) -> None:
        """Close all MCP connections."""
        for name, session in self.sessions.items():
            try:
                await session.close()
                logger.info(f"Closed connection to {name}")
            except Exception as e:
                logger.error(f"Error closing connection to {name}: {e}")

        self.sessions.clear()
        self.servers.clear()

    async def get_server_info(self, server_name: str) -> dict[str, Any]:
        """
        Get information about a connected server.

        Args:
            server_name: Name of the server

        Returns:
            Server information
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")

        session = self.sessions[server_name]

        try:
            # Get server capabilities and tools
            tools = await self.list_tools(server_name)

            return {
                "name": server_name,
                "connected": True,
                "tools_count": len(tools),
                "tools": [tool.get("name", "unknown") for tool in tools],
            }
        except Exception as e:
            logger.error(f"Failed to get info for {server_name}: {e}")
            return {"name": server_name, "connected": False, "error": str(e)}
