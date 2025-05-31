from enum import StrEnum

from core.fields.base import ReprEnum


class MCPMode(ReprEnum, StrEnum):
    """The mode to use for the MCP servers."""

    TEST = "test"
    AUTO = "auto"
    NODEJS = "nodejs"
    PYTHON = "python"


if __name__ == "__main__":
    print(MCPMode.values())
