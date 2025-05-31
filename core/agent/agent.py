from decimal import Decimal
from typing import Any

from core.agent.dependencies import AgentDependencies
from core.agent.outputs import AgentResponseOutput, DCAStrategyOutput, MarketAnalysisOutput, PortfolioStatusOutput
from core.fields import LLModel, MCPMode
from core.mcp.utils import get_mcp_servers, get_recommended_setup, get_server_capabilities
from logs.logger import get_logger
from pydantic_ai import Agent

logger = get_logger(__name__)


class PumpPieAgent:
    """
    PumpPie AI Agent powered by PydanticAI.

    This agent helps users manage Dollar Cost Averaging (DCA) investment strategies
    for cryptocurrency assets with intelligent market analysis and risk management.

    Attributes
        user_id (int): Telegram user ID
        llm (LLModel): Model to use (openai:gpt-4o, etc.). Supported models: LLModel.values()
        llm_config (dict[str, Any] | None): Optional Agent configuration
        mcp_mode (MCPMode): MCP servers mode. Supported modes: MCPMode.values()
    """

    def __init__(
        self,
        user_id: int,
        llm: LLModel = LLModel.TEST,
        llm_config: dict[str, Any] | None = None,
        mcp_mode: MCPMode = MCPMode.TEST,
    ) -> None:
        self.user_id = user_id
        self.llm = llm
        self.llm_config = llm_config or {}
        self.mcp_mode = mcp_mode

        # Get server capabilities and setup info
        self.server_capabilities = get_server_capabilities()
        self.recommended_setup = get_recommended_setup()

        self.mcp_servers = get_mcp_servers(user_id, self.mcp_mode)

        # Initialize specialized agents
        self._init_agents()

    def _init_agents(self) -> None:
        """Initialize specialized PydanticAI agents."""
        # Dependencies for dependency injection
        deps = AgentDependencies(user_id=self.user_id)

        # Conversation agent - general chat with user
        self.conversation_agent = Agent(
            model=self.llm.value,
            output_type=AgentResponseOutput,
            deps_type=AgentDependencies,
            system_prompt=self._get_conversation_prompt(),
            tools=self.mcp_servers if self.llm != LLModel.TEST else [],
        )

        # DCA strategy specialist agent
        self.dca_agent = Agent(
            model=self.llm.value,
            output_type=DCAStrategyOutput,
            deps_type=AgentDependencies,
            system_prompt=self._get_dca_prompt(),
            tools=self.mcp_servers if self.llm != LLModel.TEST else [],
        )

        # Portfolio management agent
        self.portfolio_agent = Agent(
            model=self.llm.value,
            output_type=PortfolioStatusOutput,
            deps_type=AgentDependencies,
            system_prompt=self._get_portfolio_prompt(),
            tools=self.mcp_servers if self.llm != LLModel.TEST else [],
        )

        # Market analysis agent
        self.market_agent = Agent(
            model=self.llm.value,
            output_type=MarketAnalysisOutput,
            deps_type=AgentDependencies,
            system_prompt=self._get_market_prompt(),
            tools=self.mcp_servers if self.llm != LLModel.TEST else [],
        )

    def _get_conversation_prompt(self) -> str:
        """Get system prompt for conversation agent."""
        # Dynamic prompt based on available servers
        available_tools = list(self.server_capabilities.get("supported_servers", {}).keys())
        tools_description = "\n".join(
            [
                f"        - {tool}_*: {desc}"
                for tool, desc in self.server_capabilities.get("supported_servers", {}).items()
            ]
        )

        return f"""You are PumpPie, a friendly and professional AI assistant specialized in 
        cryptocurrency investment and Dollar Cost Averaging (DCA) strategies.
        
        Your role:
        - Help users understand DCA investment strategies
        - Provide market insights and analysis
        - Guide users through portfolio management
        - Always prioritize user financial safety and education
        
        Available tools ({self.mcp_mode} mode):
{tools_description}
        
        Always be helpful, educational, and emphasize risk management."""

    def _get_dca_prompt(self) -> str:
        """Get system prompt for DCA strategy agent."""
        base_tools = """
        - market_get_asset_price: Get current crypto prices
        - market_calculate_technical_indicators: Technical analysis
        - market_analyze_volatility: Risk assessment"""

        if "db" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - db_query: Save/retrieve DCA strategies"
        if "fetch" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - fetch_get: API calls to exchanges/data providers"
        if "memory" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - memory_write: Cache analysis results"

        return f"""You are a DCA strategy specialist within PumpPie. Your expertise is creating
        and analyzing Dollar Cost Averaging investment strategies for cryptocurrency assets.
        
        Your responsibilities:
        - Analyze market conditions for DCA suitability using market_* tools
        - Create detailed DCA strategy recommendations
        - Calculate risk metrics and position sizing
        - Provide entry/exit conditions and risk management rules
        
        Always include proper risk assessment and never recommend investments beyond user's means.
        
        Available tools ({self.mcp_mode} mode):{base_tools}"""

    def _get_portfolio_prompt(self) -> str:
        """Get system prompt for portfolio agent."""
        base_tools = """
        - market_*: Current market prices and analysis"""

        if "db" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - db_query: Get user portfolio data and positions"
        if "fetch" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - fetch_get: Get additional market data"
        if "memory" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - memory_*: Cache portfolio calculations"
        if "fs" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - fs_write_file: Export portfolio reports"

        return f"""You are a portfolio management specialist within PumpPie. You analyze and 
        optimize cryptocurrency investment portfolios.
        
        Your responsibilities:
        - Analyze current portfolio performance
        - Calculate risk metrics and diversification scores
        - Provide rebalancing recommendations
        - Monitor active DCA strategies performance
        
        Available tools ({self.mcp_mode} mode):{base_tools}
        
        Focus on risk management, diversification, and long-term wealth building."""

    def _get_market_prompt(self) -> str:
        """Get system prompt for market analysis agent."""
        base_tools = """
        - market_get_asset_price: Current prices and basic info
        - market_get_price_history: Historical data
        - market_calculate_technical_indicators: RSI, SMA, EMA analysis
        - market_get_market_sentiment: Fear/greed index"""

        if "fetch" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - fetch_get: Additional API calls to data providers"
        if "memory" in self.server_capabilities.get("supported_servers", {}):
            base_tools += "\n        - memory_write: Cache analysis for performance"

        return f"""You are a market analysis specialist within PumpPie. You provide comprehensive 
        cryptocurrency market analysis and insights.
        
        Your responsibilities:
        - Analyze market trends using available tools
        - Assess market sentiment and volatility
        - Provide investment timing recommendations
        - Identify support/resistance levels and entry points
        
        Available tools ({self.mcp_mode} mode):{base_tools}
        
        Base your analysis on technical indicators, market data, and sentiment analysis."""

    async def process_message(self, message: str) -> str:
        """
        Process user message with conversation agent.

        Args:
            message: User message

        Returns:
            Agent response as string
        """
        if self.llm == LLModel.TEST:
            # Return mock response for testing
            return f"Test response to: {message}"

        try:
            deps = AgentDependencies(user_id=self.user_id)
            result = await self.conversation_agent.run(message, deps=deps)
            return result.data.response
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    async def create_dca_strategy(
        self, asset: str, amount: Decimal, interval: str, duration_months: int = 12
    ) -> DCAStrategyOutput:
        """
        Create DCA strategy with specialized agent.

        Args:
            asset: Asset symbol (e.g., BTC, ETH)
            amount: Amount to invest per interval
            interval: Investment frequency (daily, weekly, monthly)
            duration_months: Strategy duration in months

        Returns:
            Structured DCA strategy output
        """
        if self.llm == LLModel.TEST:
            # Return mock strategy for testing
            from .outputs import InvestmentRecommendation, RiskLevel

            return DCAStrategyOutput(
                strategy_id=f"dca_{self.user_id}_{asset}",
                asset=asset,
                amount_per_interval=amount,
                interval=interval,
                duration_months=duration_months,
                current_price=Decimal("50000.00"),
                risk_assessment=RiskLevel.MODERATE,
                recommendation=InvestmentRecommendation.BUY,
                total_investment=amount * Decimal(str(duration_months * 4)),  # rough weekly estimate
                expected_purchases=duration_months * 4,
                entry_conditions=["Market conditions favorable"],
                exit_conditions=["Reach target allocation"],
                explanation=f"Test DCA strategy for {asset}",
                warnings=["This is a test strategy"],
            )

        try:
            deps = AgentDependencies(user_id=self.user_id)
            prompt = f"Create a DCA strategy for {asset} with {amount} {interval} for {duration_months} months"
            result = await self.dca_agent.run(prompt, deps=deps)
            return result.data
        except Exception as e:
            logger.error(f"Error creating DCA strategy: {e}")
            raise

    async def get_portfolio_status(self) -> PortfolioStatusOutput:
        """
        Get portfolio status and analysis.

        Returns:
            Structured portfolio status output
        """
        if self.llm == LLModel.TEST:
            # Return mock portfolio for testing
            from .outputs import RiskLevel

            return PortfolioStatusOutput(
                total_value=Decimal("10000.00"),
                total_invested=Decimal("8500.00"),
                total_pnl=Decimal("1500.00"),
                total_pnl_percentage=Decimal("17.65"),
                positions=[],
                position_count=0,
                active_strategies=[],
                strategy_count=0,
                portfolio_risk=RiskLevel.MODERATE,
                diversification_score=0.65,
                largest_position_percentage=Decimal("0.00"),
                recommendations=["Test recommendation"],
                warnings=[],
                analysis_summary="Test portfolio analysis",
            )

        try:
            deps = AgentDependencies(user_id=self.user_id)
            result = await self.portfolio_agent.run("Analyze my portfolio status", deps=deps)
            return result.data
        except Exception as e:
            logger.error(f"Error getting portfolio status: {e}")
            raise

    async def get_market_analysis(self, asset: str) -> MarketAnalysisOutput:
        """
        Get market analysis for asset.

        Args:
            asset: Asset symbol to analyze

        Returns:
            Structured market analysis output
        """
        if self.llm == LLModel.TEST:
            from .outputs import InvestmentRecommendation, RiskLevel, TrendDirection

            return MarketAnalysisOutput(
                asset=asset,
                current_price=Decimal("50000.00"),
                price_change_24h=Decimal("2.5"),
                volume_24h=Decimal("25000000000"),
                market_cap=Decimal("1000000000000"),
                trend_direction=TrendDirection.BULLISH,
                trend_strength=0.75,
                volatility=Decimal("4.2"),
                technical_indicators=[],
                support_levels=[],
                resistance_levels=[],
                investment_recommendation=InvestmentRecommendation.BUY,
                dca_suitability=RiskLevel.MODERATE,
                optimal_entry_range={"min": Decimal("48000"), "max": Decimal("52000")},
                risk_factors=["Test risk"],
                opportunity_factors=["Test opportunity"],
                best_entry_timing="Current levels favorable",
                market_sentiment="Optimistic",
                detailed_analysis=f"Test analysis for {asset}",
                confidence_score=0.8,
            )

        try:
            deps = AgentDependencies(user_id=self.user_id)
            prompt = f"Analyze the market for {asset}"
            result = await self.market_agent.run(prompt, deps=deps)
            return result.data
        except Exception as e:
            logger.error(f"Error getting market analysis: {e}")
            raise

    async def health_check(self) -> dict[str, Any]:
        """
        Perform health check on agent systems.

        Returns:
            Health status information
        """
        setup_info = self.get_setup_info()

        status = {
            "user_id": self.user_id,
            "model": self.llm,
            "mcp_mode": self.mcp_mode,
            "agents_initialized": {
                "conversation": self.conversation_agent is not None,
                "dca": self.dca_agent is not None,
                "portfolio": self.portfolio_agent is not None,
                "market": self.market_agent is not None,
            },
            "mcp_servers": {
                "count": len(self.mcp_servers),
                "capabilities": self.server_capabilities,
                "servers": setup_info["server_list"],
            },
            "config": self.llm_config,
            "status": "healthy",
        }

        return status
