import cyclopts
import structlog

from ..skilltest.etl import load_data

app = cyclopts.App(help="Skilltest Zypp CLI")
logger: structlog.stdlib.BoundLogger = structlog.get_logger()


@app.command
def load():
    """Load current weather data from Buienradar API"""
    logger.info("Loading data from Buienradar API...")
    try:
        load_data()
        logger.info("Data loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")


if __name__ == "__main__":
    app()
