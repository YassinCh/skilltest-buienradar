Question 9A: Automation

Describe how you would automate the population of the database with all measurements for a specific day.
In other words, the script you created in question 1 should be used to fetch the weather station data multiple times per hour, as the weather station data is updated every 20 minutes.

Feel free to use a flowchat to show the steps of your approach.


1. I would setup Airflow and create a dag that has 2 jobs dependent of each other. The first runs the celery task command that loads weather stations, make sure that is on a 20 minute schedule using a cron expression and has retries. Preferably I would also validate that the timestamp actually matches the schedule timestamp and have it retry if it doesn't
2. I would make loading the Measurements and Wheather stations 2 independent Celery tasks and make a CeleryOperator using the python operator in Airflow to make sure we can still get the results from Celery in Airflow
3. I would use postgres as a database, and would upsert functionality to improve the current loading code this way I can use the unique constraint on weather station and timestamp to prevent duplicate entries.

This would then load new data into the database every 20 minutes