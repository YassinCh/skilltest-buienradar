# Dutch Weather Analysis - Zypp Skill Test

A Python application for collecting, analyzing, and visualizing Dutch weather data from the Buienradar API.

## 🚀 Quick Start

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management and virtual environment handling.

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd skilltest-buienradar

# Install dependencies using uv
uv sync
```

## 📊 Project Overview

This is a skill test project focusing on:

1. **Data Integration** - ETL pipeline from Buienradar API to SQLite database
2. **Data Analysis** - Weather data analysis and insights
3. **Automation/Visualization** - Automated data collection and visualization

### Key Features

- Real-time weather data collection from Buienradar API
- SQLite database with proper schema and relationships
- Modular ETL pipeline architecture
- Comprehensive data analysis capabilities
- Automated data visualization dashboard

## 🏗️ Architecture

```
src/skilltest/
├── core/                    # Core pipeline components
│   ├── extract/            # Data extraction (API sources)
│   ├── transform/          # Data transformation
│   ├── analysis/           # Data analysis tools
│   └── pipeline.py         # Main pipeline orchestration
├── buienradar/             # Buienradar-specific implementations
├── models/                 # SQLModel database models
└── database.py             # Database configuration
```

## 🔧 Usage

### Running the Data Pipeline

```bash
# Collect weather data
uv run python -m src.cli

# Or use the CLI directly
uv run python src/cli/main.py
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

## 🧪 Testing

The project includes comprehensive tests using modern pytest features.

### Running Tests

```bash
# Run all tests
PYTHONPATH=src uv run pytest

# Run with verbose output
PYTHONPATH=src uv run pytest -v

# Run specific test file
PYTHONPATH=src uv run pytest tests/src/core/test_pipeline.py -v

# Run tests by marker
PYTHONPATH=src uv run pytest -m "not slow"
PYTHONPATH=src uv run pytest -m "unit"
```

### Test Features

- **Modern pytest features**: Fixtures, parametrization, markers
- **Comprehensive mocking**: Database operations, API calls
- **Integration tests**: End-to-end pipeline testing
- **Parametrized tests**: Multiple data scenarios
- **Custom markers**: Unit, integration, slow tests

### Test Coverage

Tests cover:
- ✅ Pipeline initialization and configuration
- ✅ Data extraction from sources
- ✅ Data transformation operations
- ✅ Database operations and session management
- ✅ Error handling and edge cases
- ✅ Integration scenarios

## 📋 Data Models

### Weather Stations
- stationid (Primary Key)
- stationname
- latitude/longitude
- region

### Station Measurements
- measurementid (Generated)
- timestamp
- temperature, ground temperature, feel temperature
- wind speed, wind gusts
- humidity, precipitation
- sun power
- stationid (Foreign Key)

## 🔍 Analysis Questions Answered

- Q5: Which weather station recorded the highest temperature?
- Q6: What is the average temperature across all stations?
- Q7: Station with biggest difference between feel and actual temperature?
- Q8: Which weather station is located in the North Sea?

## 📈 Visualization

The project includes:
- Power BI dashboard (`visualization.pbix`)
- Jupyter notebook analysis (`analysis.ipynb`)
- Automated chart generation

## 🛠️ Development

### Code Quality

```bash
# Run linting (if configured)
uv run ruff check .

# Format code (if configured)
uv run ruff format .
```

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv lock --upgrade
```

### Project Structure Commands

```bash
# List all dependencies
uv pip list

# Show dependency tree
uv pip show --files package-name

# Export requirements
uv pip freeze > requirements.txt
```

## 📡 API Information

- **Buienradar JSON API**: https://json.buienradar.nl
- **Buienradar XML API**: https://xml.buienradar.nl
- **Update Frequency**: Every 20 minutes (3 times per hour)

## 🗃️ Database

- **Type**: SQLite
- **File**: `weather_data.db`
- **Migrations**: Managed with Alembic
- **Schema**: See ERD.md for entity relationship diagram

## 📝 Configuration

Configuration is managed through:
- `pyproject.toml` - Project dependencies and metadata
- `alembic.ini` - Database migration settings
- `pytest.ini` - Test configuration
- `CLAUDE.md` - Development context and guidelines

## 🚨 Troubleshooting

### Common Issues

1. **Import errors when running tests**:
   ```bash
   # Make sure PYTHONPATH includes src
   PYTHONPATH=src uv run pytest
   ```

2. **Database connection issues**:
   ```bash
   # Run migrations
   uv run alembic upgrade head
   ```

3. **API rate limiting**:
   - Buienradar updates every 20 minutes
   - Avoid excessive API calls

### Dependencies Issues

```bash
# Clear uv cache
uv cache clean

# Reinstall dependencies
rm -rf .venv uv.lock
uv sync
```

## 📄 License

This project is part of a skill test for Zypp's recruitment process.

## 🤝 Contributing

This is a skill test project with specific requirements. Follow the existing code patterns and ensure all tests pass before submitting changes.

---

**Time Cap**: 4 hours  
**Main Technologies**: Python, SQLite, uv, pytest, SQLModel, Alembic