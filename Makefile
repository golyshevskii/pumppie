#     :::::> :::::>
#    ::  :> ::  :>
#   :::::> :::::>
#  ::     ::
# :      :

# VARS
define VENV_ERROR_MSG

   (╯°□°)╯︵ ┻━┻

   Dear developer, you need to activate venv first (Python >=3.12,<3.13).
   If you don't have venv, you can setup it by command → `python3 -m venv venv`
   Then run command → `source venv/bin/activate`

   ┬─┬ノ(°-°ノ)

endef
export VENV_ERROR_MSG

# PumpPie
pp.init:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$$VENV_ERROR_MSG"; \
		exit 1; \
	fi
	pip install poetry==2.1.3
	poetry install --no-root

pp.run:
	python3 -m core.app

# Tests
agent.test:
	python3 -m tests.test_pydantic_agent

# Legacy tests
agent.test.legacy:
	python3 -m tests.test_agent_basic

# MCP Infrastructure
mcp.check:
	python tools/check_mcp_servers.py

mcp.install-official:
	npm install -g @modelcontextprotocol/server-memory
	npm install -g @modelcontextprotocol/server-fetch
	npm install -g @modelcontextprotocol/server-sqlite
	npm install -g @modelcontextprotocol/server-filesystem

# MCP Servers (manual testing)
mcp.memory:
	npx -y @modelcontextprotocol/server-memory

mcp.fetch:
	npx -y @modelcontextprotocol/server-fetch

mcp.sqlite:
	npx -y @modelcontextprotocol/server-sqlite test.db

mcp.filesystem:
	npx -y @modelcontextprotocol/server-filesystem data/

mcp.market-data:
	python3 -m core.agent.tools.market_data_server

mcp.test-server:
	python3 -m core.agent.tools.test_server

# Agent demos
agent.demo:
	python3 -c "import asyncio; from core.agent import PumpPieAgent; agent = PumpPieAgent(user_id=12345, model='test'); print('Agent created:', agent.user_id)"

agent.demo.full:
	python test_agent_quick.py

agent.demo.setup:
	python demo_agent_setup.py

# Data directories
data.init:
	mkdir -p data/logs
	mkdir -p data/exports
	mkdir -p data/databases

# Linter
lint.init:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "$$VENV_ERROR_MSG"; \
		exit 1; \
	fi
	cd linter && poetry install --no-root

lint:
	cd linter && poetry run ruff format --config pyproject.toml ../core/
	cd linter && poetry run ruff check --config pyproject.toml --fix ../core/

	cd linter && poetry run ruff format --config pyproject.toml ../tests/
	cd linter && poetry run ruff check --config pyproject.toml --fix ../tests/

lint.check:
	cd linter && poetry run ruff format --config pyproject.toml --check ../core/
	cd linter && poetry run ruff check --config pyproject.toml ../core/

	cd linter && poetry run ruff format --config pyproject.toml --check ../tests/
	cd linter && poetry run ruff check --config pyproject.toml ../tests/
