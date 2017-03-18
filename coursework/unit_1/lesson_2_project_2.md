1. The ID's and durations for the five longest trips in the data set.

```
select
	trip_id,
	duration
from
	trips
order by duration desc
limit 5
```


2. Every column of the stations table for station id 84.

```
select
	*
from
	stations
where
	station_id = 84
```

3. The dates of all the occurrences of rain in zip 94301.

```
select
	date
from
	weather
where 
	zip = 94301 AND
	events LIKE 'rain'
```