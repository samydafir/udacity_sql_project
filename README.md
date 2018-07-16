# README

### Description
This program retrieves information about authors, articles and page faults
and presents them in a formatted way. The output includes the top three
articles of all time by views, the top authors of all time, taking
into account views of their written articles and a list of days on which
more than 1 percent of requests lead to errors (4xx, 5xx status code).

The application fetches data from a postgresql database using psycopg2.
All calculations to retrieve the final result tuples are done by the database.
Python only handles sending database queries as well as output formatting.


### Requirements
+ `python3`
+ `psycopg2`

### Execution
`python log_analysis.py`
