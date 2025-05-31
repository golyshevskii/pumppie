#!/usr/bin/env python3
"""Test MCP server for PumpPie agent."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("pumppie-test-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back the input message",
            inputSchema={
                "type": "object",
                "properties": {"message": {"type": "string", "description": "Message to echo back"}},
                "required": ["message"],
            },
        ),
        Tool(
            name="get_time",
            description="Get current timestamp",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="calculate",
            description="Perform basic arithmetic calculation",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2')",
                    }
                },
                "required": ["expression"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Call a tool with given arguments."""
    if name == "echo":
        message = arguments.get("message", "")
        return [{"type": "text", "text": f"Echo: {message}"}]

    elif name == "get_time":
        import datetime

        current_time = datetime.datetime.now().isoformat()
        return [{"type": "text", "text": f"Current time: {current_time}"}]

    elif name == "calculate":
        expression = arguments.get("expression", "")
        try:
            # Safe evaluation of basic arithmetic
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return [{"type": "text", "text": f"Result: {expression} = {result}"}]
            else:
                return [{"type": "text", "text": f"Error: Invalid characters in expression: {expression}"}]
        except Exception as e:
            return [{"type": "text", "text": f"Error calculating {expression}: {str(e)}"}]

    else:
        return [{"type": "text", "text": f"Unknown tool: {name}"}]


async def main():
    """Run the MCP server."""
    logger.info("Starting PumpPie test MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
