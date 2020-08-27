dates = []
dates.append(дата1)
dates.append(дата2)



SELECT result
COUNT(*)
FROM <table_name>
GROUP BY result
WHERE  dates[0] <= DATE(date) AND date <= dates[1]


SELECT
*
FROM project, server, <table_name>
WHERE dates[0] <= Date AND Date <= dates[1]