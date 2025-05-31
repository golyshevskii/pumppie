# PumpPie AI Agent Architecture (PydanticAI Edition)

## Overview

PumpPie AI Agent теперь построен на **PydanticAI** - современном Python фреймворке для создания продакшн-готовых AI-агентов. Это обеспечивает типобезопасность, структурированные ответы, валидацию данных и встроенную поддержку MCP (Model Context Protocol).

## Why PydanticAI?

### Преимущества:

- **🔥 FastAPI-подобная эргономика** для разработки AI-агентов
- **🛡️ Типобезопасность** с полной поддержкой Pydantic v2
- **📊 Structured Outputs** с автоматической валидацией
- **🔌 Встроенная MCP поддержка** для работы с внешними инструментами
- **🧪 Dependency Injection** для тестирования и модульности
- **📈 Streaming поддержка** для real-time ответов
- **🎯 Multi-agent системы** с специализированными агентами

## Architecture Components

### 1. Main Agent (`core/agent/pydantic_agent.py`)

#### PumpPieAgent

Основной класс агента, который включает в себя **4 специализированных агента**:

- `conversation_agent` - общение с пользователем
- `dca_agent` - создание DCA стратегий
- `portfolio_agent` - анализ портфеля
- `market_agent` - анализ рынка

**Ключевые особенности:**

```python
class PumpPieAgent:
    def __init__(self, user_id: int, model: str = "openai:gpt-4o"):
        # Автоматическая настройка MCP серверов
        self.mcp_servers = [
            MCPServerStdio("python", args=["-m", "core.agent.tools.market_data_server"], tool_prefix="market"),
            MCPServerStdio("python", args=["-m", "core.agent.tools.portfolio_server"], tool_prefix="portfolio"),
            MCPServerStdio("python", args=["-m", "core.agent.tools.dca_server"], tool_prefix="dca")
        ]
      
        # Специализированные агенты с типизированными выходами
        self.conversation_agent = Agent(model, output_type=AgentResponseOutput, ...)
        self.dca_agent = Agent(model, output_type=DCAStrategyOutput, ...)
```

### 2. Dependencies System (`core/agent/dependencies.py`)

#### AgentDependencies

Система dependency injection для чистой архитектуры:

```python
@dataclass
class AgentDependencies:
    user_id: int
  
    async def get_user_config(self, user_id: int) -> Dict[str, Any]
    async def get_user_portfolio(self, user_id: int) -> Dict[str, Any]
    async def save_dca_strategy(self, strategy_data: Dict[str, Any]) -> str
    async def get_market_data(self, asset: str) -> Dict[str, Any]
```

### 3. Typed Outputs (`core/agent/outputs.py`)

#### Структурированные выходные данные с валидацией:

**DCAStrategyOutput** - результат создания DCA стратегии:

```python
class DCAStrategyOutput(BaseModel):
    strategy_id: str
    asset: str
    amount_per_interval: Decimal
    risk_assessment: RiskLevel
    recommendation: InvestmentRecommendation
    total_investment: Decimal
    # ... и многое другое с полной типизацией
```

**PortfolioStatusOutput** - статус портфеля:

```python
class PortfolioStatusOutput(BaseModel):
    total_value: Decimal
    total_pnl_percentage: Decimal
    positions: List[PortfolioPosition]
    portfolio_risk: RiskLevel
    recommendations: List[str]
```

**MarketAnalysisOutput** - анализ рынка:

```python
class MarketAnalysisOutput(BaseModel):
    asset: str
    trend_direction: TrendDirection
    investment_recommendation: InvestmentRecommendation
    technical_indicators: List[TechnicalIndicator]
    confidence_score: float
```

### 4. MCP Tools Integration

#### Встроенные MCP серверы:

**Market Data Server** (`core/agent/tools/market_data_server.py`):

- `get_asset_price` - текущие цены и базовая информация
- `get_price_history` - исторические данные для технического анализа
- `calculate_technical_indicators` - RSI, SMA, EMA, волатильность
- `get_market_sentiment` - индекс страха/жадности, настроения рынка
- `analyze_volatility` - анализ рисков и волатильности

**Portfolio Server** (запланирован):

- Управление портфелем пользователя
- Отслеживание позиций и P&L
- Анализ диверсификации

**DCA Server** (запланирован):

- Создание и управление DCA стратегиями
- Автоматическое выполнение покупок
- Мониторинг стратегий

## Usage Examples

### Базовое использование

```python
import asyncio
from core.agent import PumpPieAgent

async def main():
    # Создание агента
    agent = PumpPieAgent(user_id=12345, model="openai:gpt-4o")
  
    # Общение с пользователем
    response = await agent.process_message("Создай DCA стратегию для BTC на $100 в неделю")
    print(response)
  
    # Создание DCA стратегии с типизированным выходом
    strategy = await agent.create_dca_strategy(
        asset="BTC",
        amount=Decimal("100"),
        interval="weekly",
        duration_months=12
    )
    print(f"Стратегия создана: {strategy.strategy_id}")
    print(f"Риск: {strategy.risk_assessment}")
    print(f"Рекомендация: {strategy.recommendation}")
  
    # Анализ портфеля
    portfolio = await agent.get_portfolio_status()
    print(f"Общая стоимость: ${portfolio.total_value}")
    print(f"P&L: {portfolio.total_pnl_percentage}%")
  
    # Анализ рынка
    analysis = await agent.get_market_analysis("BTC")
    print(f"Тренд: {analysis.trend_direction}")
    print(f"Рекомендация: {analysis.investment_recommendation}")

asyncio.run(main())
```

### Динамические System Prompts

```python
@agent.conversation_agent.system_prompt
async def add_user_context(ctx: RunContext[AgentDependencies]) -> str:
    user_config = await ctx.deps.get_user_config(ctx.deps.user_id)
    return f"User preferences: {user_config.get('risk_tolerance', 'moderate')}"
```

## Testing

### Comprehensive Test Suite

```bash
# Новые PydanticAI тесты
make agent.test

# Legacy тесты (для совместимости)
make agent.test.legacy

# MCP серверы
make mcp.market-data

# Демо агента
make agent.demo
```

### Test Features

- **Fixture-based testing** с pytest
- **Mock данные** для всех MCP инструментов
- **Validation testing** для Pydantic моделей
- **Integration testing** для MCP серверов
- **Health checks** для monitoring

## Key Benefits

### 🚀 **Производительность**

- Типизированные выходы устраняют парсинг и валидацию
- Встроенная поддержка streaming для real-time ответов
- Эффективная работа с MCP протоколом

### 🛡️ **Надежность**

- Полная типобезопасность с Pydantic v2
- Автоматическая валидация всех входов и выходов
- Структурированное логирование и error handling

### 🧪 **Тестируемость**

- Dependency injection для изоляции компонентов
- Test models для development без API вызовов
- Comprehensive test coverage

### 🔧 **Расширяемость**

- Легкое добавление новых MCP инструментов
- Модульная архитектура агентов
- Plugin-based system для новых возможностей

## Migration from Legacy

### Основные изменения:

```python
# БЫЛО (legacy):
from core.agent.base import PPAgent

agent = PPAgent(user_id=123)
response = await agent.process_message("Hello")
# response - простая строка

# СТАЛО (PydanticAI):
from core.agent import PumpPieAgent

agent = PumpPieAgent(user_id=123, model="openai:gpt-4o")
response = await agent.process_message("Hello") 
# response - строка, но внутри AgentResponseOutput с валидацией

# Типизированные выходы:
strategy = await agent.create_dca_strategy("BTC", Decimal("100"), "weekly")
# strategy - полностью типизированный DCAStrategyOutput объект
```

## Next Steps

### Immediate (Q1 2025):

1. ✅ **Базовая PydanticAI архитектура**
2. ✅ **MCP интеграция с market data**
3. 🔄 **Portfolio и DCA MCP серверы**
4. 🔄 **Real API интеграции** (CoinGecko, exchanges)

### Medium-term (Q2 2025):

1. **Database интеграция** для состояния пользователей
2. **Advanced MCP tools** (risk management, backtesting)
3. **Multi-model support** (Claude, Gemini, локальные модели)
4. **Production monitoring** с Pydantic Logfire

### Long-term (Q3-Q4 2025):

1. **Multi-agent workflows** с оркестрацией
2. **Real-time trading** интеграция
3. **Advanced analytics** и ML предсказания
4. **Mobile app** интеграция

## Current Status

### ✅ **Completed:**

- PydanticAI базовая архитектура
- Типизированные выходные модели
- MCP market data сервер
- Comprehensive testing suite
- Documentation

### 🔄 **In Progress:**

- Portfolio MCP сервер
- DCA MCP сервер
- Real market data API интеграция

### ❌ **Pending:**

- Database модели и интеграция
- Production deployment
- Exchange API интеграция
- Advanced risk management tools

---

**Архитектура PumpPie на PydanticAI обеспечивает production-ready решение с современными практиками разработки, полной типобезопасностью и отличной developer experience.**
