# Claude Assistant Context for Zypp Skill Test: Dutch Weather Analysis

## Project Overview
This is a skill test project for Zypp's recruitment process focused on Dutch weather data analysis using the Buienradar API.

## Key Information
- **Time Cap**: 4 hours
- **Main Skills**: Python, SQL, optional: HTML/CSS/JavaScript
- **Focus Areas**: Data Integration, Data Modeling, Data Analysis, Automation/Visualization

## Project Structure
The project consists of 3 main parts:
1. **Data Integration** (2 hours) - ETL from Buienradar API to SQL database
2. **Data Analysis** (1 hour) - Answering questions using collected data
3. **Automation or Data Visualization** (1 hour) - Either automate data collection or visualize results

## Technical Details

### API Endpoints
- JSON: https://json.buienradar.nl
- XML: https://xml.buienradar.nl
- Update frequency: 3 times per hour (every 20 minutes)

### Required Data Models
1. **Station Measurements Table**:
   - measurementid (generate this)
   - timestamp
   - temperature
   - groundtemperature
   - feeltemperature
   - windgusts
   - windspeedBft
   - humidity
   - precipitation
   - sunpower
   - stationid (FK)

2. **Weather Stations Table**:
   - stationid (PK)
   - stationname
   - lat
   - lon
   - regio

### Database Requirements
- Use SQLite (.sqlite file)
- Implement proper indexes and primary keys
- Define relationships between tables
- Database file must be committed to repository

### Analysis Questions to Answer
- Q5: Which weather station recorded the highest temperature?
- Q6: What is the average temperature?
- Q7: What is the station with the biggest difference between feel temperature and actual temperature?
- Q8: Which weather station is located in the North Sea?

### Development Guidelines
- Use Python 3.10+
- Make code reproducible
- Commit all solutions including the database
- Fork the repository before starting

## Important Notes
- The Buienradar API provides current weather data for all Dutch weather stations
- Data needs to be collected over time to build a full day's dataset
- Consider automation for collecting data throughout the day
- ERD diagram can be created using draw.io

## Testing/Verification Commands
Since no specific test commands were found in the README, consider implementing:
- Data validation scripts
- Query result verification
- API connection tests

## Project Status
- Current branch: main
- Untracked files: main.py, pyproject.toml, uv.lock
- Repository is a git repo with recent commits related to question renaming