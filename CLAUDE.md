# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Dutch weather data analysis project that collects, processes, and analyzes weather data from the Buienradar API. It's a skill test project with a 4-hour time cap, focusing on ETL pipelines, data analysis, and visualization.

## Essential Commands

### Development Environment
```bash
# Install dependencies and set up environment
uv sync

uv run python -m src.cli
# or
uv run python src/cli/main.py
```

### Testing
```bash
# Run all tests (IMPORTANT: Always include PYTHONPATH)
PYTHONPATH=src uv run pytest

# Run with verbose output
PYTHONPATH=src uv run pytest -v

# Run specific test file
PYTHONPATH=src uv run pytest tests/src/core/test_pipeline.py -v

# Run by test markers
PYTHONPATH=src uv run pytest -m "unit"
PYTHONPATH=src uv run pytest -m "integration"
PYTHONPATH=src uv run pytest -m "not slow"
```

### Database Operations
```bash
# Run database migrations
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "description"
```

### Data Analysis
```bash
# Start Jupyter notebook for analysis
uv run jupyter notebook analysis.ipynb
```

### Code Quality (if available)
```bash
# Check code with ruff (if configured)
uv run ruff check .

# Format code with ruff (if configured)
uv run ruff format .
```

## Architecture Overview

This project follows a modular ETL pipeline architecture:

### Core Pipeline System (`src/skilltest/core/`)
- **Pipeline**: Generic pipeline orchestrator that chains data sources and transformers
- **Extract**: Data extraction layer with `AbstractSource` and `HttpSource` for API calls
- **Transform**: Data transformation layer with various transformer types:
  - `FromJsonToEntryTransformer`: Extracts nested JSON data
  - `DictToPydanticTransformer`: Converts dicts to Pydantic models
  - `PydanticToPydanticTransformer`: Transforms between Pydantic models
- **Analysis**: Data analysis utilities with dataframe conversion

### Buienradar Implementation (`src/skilltest/buienradar/`)
- **BuienradarPipeline**: Complete weather data pipeline implementation
- **Schema**: Pydantic models for API response structure
- Implements two parallel pipelines: weather stations and measurements

### Database Layer
- **SQLModel** for ORM with SQLite backend
- **Alembic** for database migrations
- Database file: `weather_data.db`
- Models: WeatherStation and Measurement with proper relationships

### CLI Interface (`src/cli/`)
- **Cyclopts** for command-line interface
- **Structlog** for structured logging
- Main command: `load_data` to run the data collection pipeline

## Key Patterns

### Pipeline Pattern
The core uses a generic Pipeline class that allows chaining of transformers:
```python
pipeline = Pipeline(source).add(transformer1).add(transformer2)
pipeline.run()
```

### Data Flow
1. HttpSource fetches JSON from Buienradar API
2. FromJsonToEntryTransformer extracts station measurements
3. DictToPydanticTransformer converts to schema objects
4. PydanticToPydanticTransformer splits into WeatherStation and Measurement models
5. Pipeline saves to SQLite using session.merge() for upserts

### Testing Strategy
- Comprehensive pytest setup with custom markers (unit, integration, slow)
- Mocking of database operations and API calls
- Parametrized tests for multiple scenarios
- Test configuration in `pytest.ini` with strict markers

## Important Notes

### PYTHONPATH Requirement
Always set `PYTHONPATH=src` when running tests or the application may fail to import modules correctly.

### Database Migrations
Use Alembic for all schema changes. The SQLite database is configured in `alembic.ini`.

### API Considerations
- Buienradar API updates every 20 minutes
- Avoid excessive API calls to prevent rate limiting
- API URL configured in settings: https://json.buienradar.nl

### Uv Package Manager
This project uses `uv` for fast Python package management instead of pip/virtualenv.

## Development Workflow

1. Make changes to source code in `src/skilltest/`
2. Run tests with `PYTHONPATH=src uv run pytest -v`
3. Test the CLI with `uv run python -m src.cli`
4. Create database migrations if models changed: `uv run alembic revision --autogenerate -m "description"`
5. Run migrations: `uv run alembic upgrade head`

## Project Constraints

- Time cap: 4 hours for skill test
- Focus on data integration, analysis, and automation/visualization
- SQLite database for simplicity
- Modern Python practices with type hints and structured logging