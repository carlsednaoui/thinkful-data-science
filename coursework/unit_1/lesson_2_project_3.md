1. What was the hottest day? Where was that?

```
select
	maxtemperaturef,
	zip
from
	weather
order by maxtemperaturef desc
limit 1
```

2. How many trips started at each station?

```
select
	start_station,
	count(trip_id)
from
	trips
group by 	start_station
order by 2 desc
```

3. What's the shortest trip that happened?
=> Shortest in terms of distance or duration?

```
select
	*
from
	trips
order by duration
limit 1

-- the result is duration = 100. More than one trip had a duration of 100

select
	count(*)
from
	trips
where duration = 100
```

4. What is the average trip duration, by end station?

```
select
	end_station,
	avg(duration)
from
	trips
group by end_station
order by 2 desc
```