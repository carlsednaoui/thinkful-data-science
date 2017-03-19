1. What are the three longest trips on rainy days?

```
select
	w.events,
	CAST (t.duration as INT)
from
	weather w
join
	trips t
on
	w.zip = t.zip_code
where 
	w.events = 'Rain'
order by 2 desc
limit 3
```


2. What is the average number of open docks in each station on days where it is raining in that zip code?

My computer crashed trying to run this... lol: https://cl.ly/292G1l2R0t3v

I tried adding indexes but still nada

```
-- 2. What is the average number of open docks in each station on days where it is raining in that zip code?

-- Even this query is not completing...

select
	stations.name,
	avg(status.docks_available)
from 
	status
join
	stations
on
	stations.station_id = status.station_id
group by
	stations.name


-- My final query would look like this. Unfortunately I can't QA this :(

select
	stations.name,
	avg(status.docks_available)
from 
	status
join
	stations
on
	stations.station_id = status.station_id
join
	trips
on
	trips.start_station = stations.name
join
	weather
on
	trips.zip_code = weather.zip_code
where
	weather.event = 'Rain'
group by
	stations.name

```


3. Which station is empty most often?

```
select
	station_id,
	avg(docks_available)
from
	status
group by
	station_id
```