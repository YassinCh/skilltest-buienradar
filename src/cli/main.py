import cyclopts
import structlog

from src.skilltest.buienradar import BuienradarPipeline
from src.skilltest.weather_analysis import WeatherAnalysis

app = cyclopts.App(help="Skilltest Zypp CLI")
logger: structlog.stdlib.BoundLogger = structlog.get_logger()


@app.command
def load_data():
    """Load current weather data from Buienradar API"""
    logger.info("Loading data from Buienradar API...")
    try:
        pipeline = BuienradarPipeline()
        pipeline.run()
        logger.info("Data loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")


@app.command
def analyze_highest_temp():
    """Find weather station with highest temperature (Question 5)"""
    logger.info("Finding station with highest temperature...")
    try:
        analysis = WeatherAnalysis()
        result = analysis.highest_temperature_station()
        
        if result:
            logger.info(
                f"Highest temperature recorded:",
                station=result.get('stationname'),
                temperature=result.get('temperature'),
                timestamp=result.get('timestamp')
            )
        else:
            logger.warning("No temperature data found in database")
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")


@app.command
def analyze_average_temp():
    """Calculate average temperature (Question 6)"""
    logger.info("Calculating average temperature...")
    try:
        analysis = WeatherAnalysis()
        avg_temp = analysis.average_temperature()
        
        if avg_temp is not None:
            logger.info(f"Average temperature: {avg_temp:.2f}°C")
        else:
            logger.warning("No temperature data found in database")
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")


@app.command
def analyze_feel_difference():
    """Find station with biggest feel temperature difference (Question 7)"""
    logger.info("Finding station with biggest feel temperature difference...")
    try:
        analysis = WeatherAnalysis()
        result = analysis.biggest_feel_temp_difference()
        
        if result:
            logger.info(
                f"Biggest feel temperature difference:",
                station=result.get('stationname'),
                actual_temp=result.get('temperature'),
                feel_temp=result.get('feeltemperature'),
                difference=result.get('temp_diff')
            )
        else:
            logger.warning("No temperature data found in database")
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")


@app.command
def analyze_north_sea():
    """Find weather station in North Sea (Question 8)"""
    logger.info("Finding North Sea weather station...")
    try:
        analysis = WeatherAnalysis()
        result = analysis.north_sea_station()
        
        if result:
            logger.info(
                f"North Sea station found:",
                station=result.get('stationname'),
                region=result.get('regio'),
                coordinates=f"({result.get('lat')}, {result.get('lon')})"
            )
        else:
            logger.warning("No North Sea station found in database")
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")


@app.command
def analyze_all():
    """Run all analysis questions (5-8)"""
    logger.info("Running all analysis questions...")
    try:
        analysis = WeatherAnalysis()
        results = analysis.get_all_analysis_results()
        
        # Question 5
        if results['question_5_highest_temp']:
            r = results['question_5_highest_temp']
            logger.info(f"Q5 - Highest temperature: {r['stationname']} - {r['temperature']}°C")
        
        # Question 6
        if results['question_6_avg_temp'] is not None:
            logger.info(f"Q6 - Average temperature: {results['question_6_avg_temp']:.2f}°C")
        
        # Question 7
        if results['question_7_biggest_feel_diff']:
            r = results['question_7_biggest_feel_diff']
            logger.info(f"Q7 - Biggest feel difference: {r['stationname']} - {r['temp_diff']:.2f}°C")
        
        # Question 8
        if results['question_8_north_sea']:
            r = results['question_8_north_sea']
            logger.info(f"Q8 - North Sea station: {r['stationname']} in {r['regio']}")
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")


if __name__ == "__main__":
    app()
