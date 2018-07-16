#!/usr/bin/python3

import psycopg2


def pop_articles(c):
    """Returns the three most popular articles of all time. Receives a cursor
    as argument. Prints articles and views
    """
    print("Top three articles of all time:")
    query = """SELECT art.title, count(art.title) AS views
               FROM articles AS art,
               (SELECT REPLACE (path, '/article/', '')
                 AS article FROM log ) AS l
               WHERE art.slug = l.article
               GROUP BY art.title
               ORDER BY views DESC;
    """
    c.execute(query)
    row = c.fetchone()
    count = 0
    while row is not None and count < 3:
        print('"' + row[0] + '" - ' + str(row[1]) + " views")
        row = c.fetchone()
        count += 1


def pop_authors(c):
    """Returns the most popular authors of all time. Each author and all views
    of their articles, sorted by number of views. Receives a cursor as argument
    """
    print("Most popular authors of all time:")
    query = """SELECT auth.name, count(auth.name) as views
               FROM authors AS auth, articles AS art,
               (SELECT REPLACE (path, '/article/', '')
                 AS article FROM log ) AS l
               WHERE auth.id = art.author
               AND art.slug = l.article
               GROUP BY auth.name
               ORDER BY views DESC;
    """
    c.execute(query)
    row = c.fetchone()
    while row is not None:
        print(row[0] + " - " + str(row[1]) + " views")
        row = c.fetchone()


def top_error_days(c):
    """Lists days on which more than 1% of all page requests lead to errors and
       the corresponding error percentage. All calculations done by the
       database. receives a cursor as argument.
    """
    print("Days with more than 1% request errors:")
    query = """SELECT all_logs.day, 100.0*error_logs.views/all_logs.views
    FROM
    (SELECT time::date as day, count(time::date) AS views
    FROM log
    GROUP BY time::date
    ORDER BY time::date ASC) as all_logs,
    (SELECT time::date as day, count(time::date) AS views
    FROM log
    WHERE status like '4%' OR status like '5%'
    GROUP BY time::date
    ORDER BY time::date ASC) as error_logs
    WHERE all_logs.day = error_logs.day

    """

    c.execute(query)
    row = c.fetchone()
    while row is not None:
        if row[1] > 1:
            print(str(row[0]) + " - " + '{:.2f}'.format(row[1],) + "%")
        row = c.fetchone()


# Create db connection and cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()
# print output
pop_articles(c)
print("\n")
pop_authors(c)
print("\n")
top_error_days(c)

# close cursor and connection
c.close()
db.close()
