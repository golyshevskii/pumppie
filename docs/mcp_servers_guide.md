# PumpPie MCP Servers Guide

## Overview

PumpPie использует комбинацию **официальных MCP серверов** от Anthropic и **кастомных серверов** для максимальной функциональности. Благодаря интеграции с [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) мы получаем доступ к готовым, проверенным решениям.

## Available Servers

### 🏢 Official Servers (Node.js)

Эти серверы доступны при наличии Node.js и устанавливаются автоматически:

#### 1. **Memory Server** (`@modelcontextprotocol/server-memory`)
- **Назначение**: Кэширование данных в памяти между вызовами
- **Команды**: `memory_write`, `memory_read`, `memory_delete`
- **Использование**: Сохранение анализа рынка, пользовательских настроек
- **Установка**: `npx -y @modelcontextprotocol/server-memory`

#### 2. **Fetch Server** (`@modelcontextprotocol/server-fetch`)
- **Назначение**: HTTP запросы к внешним API
- **Команды**: `fetch_get`, `fetch_post`
- **Использование**: Интеграция с биржами, получение real-time данных
- **Установка**: `npx -y @modelcontextprotocol/server-fetch`

#### 3. **SQLite Server** (`@modelcontextprotocol/server-sqlite`)
- **Назначение**: Локальная база данных для персистентности
- **Команды**: `db_query`, `db_execute`
- **Использование**: Хранение портфелей, DCA стратегий, истории
- **Установка**: `npx -y @modelcontextprotocol/server-sqlite`

#### 4. **Filesystem Server** (`@modelcontextprotocol/server-filesystem`)
- **Назначение**: Операции с файлами
- **Команды**: `fs_read_file`, `fs_write_file`, `fs_list_directory`
- **Использование**: Экспорт отчетов, логирование, бэкапы
- **Установка**: `npx -y @modelcontextprotocol/server-filesystem`

### 🐍 Custom Python Servers

Наши специализированные серверы для крипто-анализа:

#### 1. **Market Data Server** (`core.agent.tools.market_data_server`)
- **Назначение**: Анализ криптовалютных рынков
- **Команды**: 
  - `market_get_asset_price` - текущие цены
  - `market_get_price_history` - исторические данные
  - `market_calculate_technical_indicators` - технический анализ
  - `market_get_market_sentiment` - индекс страха/жадности
  - `market_analyze_volatility` - анализ рисков
- **Использование**: Основа для всех инвестиционных решений

## Configuration Modes

### 🎯 Auto Mode (Recommended)
```python
agent = PumpPieAgent(user_id=123, model="openai:gpt-4o", mcp_mode="auto")
```
- Автоматически определяет доступные серверы
- Использует все доступные возможности
- **Требует**: Node.js + Python

### 🐍 Python Mode (Limited)
```python
agent = PumpPieAgent(user_id=123, model="openai:gpt-4o", mcp_mode="python")
```
- Только Python серверы
- Ограниченная функциональность
- **Требует**: только Python

### 🧪 Test Mode (Development)
```python
agent = PumpPieAgent(user_id=123, model="test", mcp_mode="test")
```
- Без MCP серверов
- Mock данные
- Быстрая разработка

## Setup Instructions

### Quick Setup

```bash
# 1. Проверить текущие возможности
make mcp.check

# 2. Установить Node.js серверы (если есть Node.js)
make mcp.install-official

# 3. Создать директории для данных
make data.init

# 4. Протестировать конфигурацию
make agent.demo.setup
```

### Manual Setup

#### Для полной функциональности:

```bash
# 1. Установить Node.js (если нет)
# Windows: скачать с https://nodejs.org/
# macOS: brew install node
# Linux: apt install nodejs npm

# 2. Установить официальные MCP серверы
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-sqlite
npm install -g @modelcontextprotocol/server-filesystem

# 3. Проверить установку
npx -y @modelcontextprotocol/server-memory --help
```

#### Для Python-only режима:
```bash
# Готово! Просто используйте mcp_mode="python"
```

## Usage Examples

### 1. Market Analysis with Full Stack

```python
from core.agent import PumpPieAgent

# Полная конфигурация с всеми серверами
agent = PumpPieAgent(
    user_id=12345, 
    model="openai:gpt-4o",
    mcp_mode="auto"  # Автоопределение серверов
)

# Агент автоматически использует:
# - market_* для анализа
# - memory_* для кэширования
# - db_* для сохранения результатов
# - fetch_* для дополнительных данных
analysis = await agent.get_market_analysis("BTC")
```

### 2. DCA Strategy with Persistence

```python
# Создание стратегии с сохранением в БД
strategy = await agent.create_dca_strategy(
    asset="BTC",
    amount=Decimal("100"),
    interval="weekly",
    duration_months=12
)

# Стратегия автоматически сохраняется в SQLite
# через db_* команды
```

### 3. Portfolio Export

```python
# Получение статуса портфеля
portfolio = await agent.get_portfolio_status()

# Экспорт отчета через filesystem server
# Автоматически сохраняется в data/reports/
```

## Server Capabilities Matrix

| Feature | Test Mode | Python Mode | Auto Mode (with Node.js) |
|---------|-----------|-------------|---------------------------|
| Market Data | ✅ Mock | ✅ Real | ✅ Real |
| Technical Analysis | ✅ Mock | ✅ Real | ✅ Real |
| Data Persistence | ❌ | ❌ | ✅ SQLite |
| External API Calls | ❌ | ❌ | ✅ HTTP |
| File Operations | ❌ | ❌ | ✅ Files |
| Memory Caching | ❌ | ❌ | ✅ RAM |
| Performance | 🔥 Fast | ⚡ Good | 🚀 Best |

## Community Servers (Future)

Из [репозитория](https://github.com/modelcontextprotocol/servers) мы планируем интегрировать:

### Потенциальные интеграции:
- **PostgreSQL Server** - для production БД
- **GitHub Server** - для логирования стратегий в Git
- **Web Scraping** серверы - для новостей и sentiment
- **Slack/Discord** серверы - для уведомлений
- **PDF/Document** серверы - для отчетности

### Crypto-specific серверы:
- Ищем готовые серверы для интеграции с биржами
- Планируем создать серверы для популярных API (Binance, Coinbase)

## Troubleshooting

### Node.js not found
```bash
# Проверить установку
node --version
npm --version

# Если нет - установить Node.js
# https://nodejs.org/
```

### MCP Server installation fails
```bash
# Обновить npm
npm install -g npm@latest

# Попробовать альтернативную установку
npx -y @modelcontextprotocol/server-memory
```

### Slow performance
```bash
# Использовать memory server для кэширования
agent = PumpPieAgent(mcp_mode="auto")  # включит кэширование
```

## Next Steps

1. **Immediate**: Настроить полную конфигурацию с Node.js
2. **Short-term**: Интегрировать PostgreSQL server для production
3. **Medium-term**: Добавить community серверы для расширения функций
4. **Long-term**: Создать собственные серверы для крипто-экосистемы

---

**Правильная настройка MCP серверов критически важна для production использования PumpPie. Следуйте этому руководству для максимальной эффективности агента.** 