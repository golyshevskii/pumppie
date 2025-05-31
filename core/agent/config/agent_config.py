"""PumpPie Agent configuration."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MCPServerConfig:
    """Configuration for MCP server."""

    name: str
    command: str
    args: list[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class DCAConfig:
    """DCA strategy configuration."""

    min_amount: float = 1.0
    max_amount: float = 10000.0
    supported_intervals: list[str] = field(default_factory=lambda: ["daily", "weekly", "monthly"])
    default_interval: str = "weekly"

    # Smart DCA parameters
    volatility_threshold: float = 0.05  # 5% volatility threshold
    rsi_oversold: int = 30
    rsi_overbought: int = 70


@dataclass
class RiskManagementConfig:
    """Risk management configuration."""

    max_portfolio_allocation: float = 0.8  # Max 80% of portfolio in crypto
    max_single_asset_allocation: float = 0.3  # Max 30% in single asset
    stop_loss_threshold: float = -0.2  # Stop if asset drops 20%
    take_profit_threshold: float = 2.0  # Take profit at 200% gain


@dataclass
class AgentConfig:
    """Main agent configuration."""

    # User settings
    user_id: int
    language: str = "en"

    # MCP servers
    mcp_servers: list[MCPServerConfig] = field(default_factory=list)

    # Strategy configs
    dca_config: DCAConfig = field(default_factory=DCAConfig)
    risk_management: RiskManagementConfig = field(default_factory=RiskManagementConfig)

    # Agent behavior
    auto_rebalance: bool = True
    rebalance_frequency: str = "weekly"  # daily, weekly, monthly
    notifications_enabled: bool = True

    # Exchange settings
    exchange: str | None = None
    api_key_encrypted: str | None = None

    @classmethod
    def create_default(cls, user_id: int) -> "AgentConfig":
        """
        Create default agent configuration.

        Args:
            user_id: Telegram user ID

        Returns:
            Default AgentConfig instance
        """
        return cls(
            user_id=user_id,
            mcp_servers=[
                MCPServerConfig(
                    name="market_data",
                    command="python",
                    args=["-m", "core.agent.tools.market_data"],
                    enabled=False,  # Will enable when implemented
                ),
                MCPServerConfig(
                    name="portfolio",
                    command="python",
                    args=["-m", "core.agent.tools.portfolio"],
                    enabled=False,  # Will enable when implemented
                ),
            ],
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert config to dictionary.

        Returns:
            Configuration as dictionary
        """
        return {
            "user_id": self.user_id,
            "language": self.language,
            "mcp_servers": [
                {"name": server.name, "command": server.command, "args": server.args, "enabled": server.enabled}
                for server in self.mcp_servers
            ],
            "dca_config": {
                "min_amount": self.dca_config.min_amount,
                "max_amount": self.dca_config.max_amount,
                "supported_intervals": self.dca_config.supported_intervals,
                "default_interval": self.dca_config.default_interval,
                "volatility_threshold": self.dca_config.volatility_threshold,
                "rsi_oversold": self.dca_config.rsi_oversold,
                "rsi_overbought": self.dca_config.rsi_overbought,
            },
            "risk_management": {
                "max_portfolio_allocation": self.risk_management.max_portfolio_allocation,
                "max_single_asset_allocation": self.risk_management.max_single_asset_allocation,
                "stop_loss_threshold": self.risk_management.stop_loss_threshold,
                "take_profit_threshold": self.risk_management.take_profit_threshold,
            },
            "auto_rebalance": self.auto_rebalance,
            "rebalance_frequency": self.rebalance_frequency,
            "notifications_enabled": self.notifications_enabled,
            "exchange": self.exchange,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentConfig":
        """
        Create config from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            AgentConfig instance
        """
        mcp_servers = [MCPServerConfig(**server_data) for server_data in data.get("mcp_servers", [])]

        dca_data = data.get("dca_config", {})
        dca_config = DCAConfig(**dca_data)

        risk_data = data.get("risk_management", {})
        risk_config = RiskManagementConfig(**risk_data)

        return cls(
            user_id=data["user_id"],
            language=data.get("language", "en"),
            mcp_servers=mcp_servers,
            dca_config=dca_config,
            risk_management=risk_config,
            auto_rebalance=data.get("auto_rebalance", True),
            rebalance_frequency=data.get("rebalance_frequency", "weekly"),
            notifications_enabled=data.get("notifications_enabled", True),
            exchange=data.get("exchange"),
        )
