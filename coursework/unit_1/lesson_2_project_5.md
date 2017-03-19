1. What's the most expensive listing? What else can you tell me about the listing?

A 4 bedroom apartment in the greenwich village costs $999 per day. The review score is 100%!

```
select
	max(cast(trim(trim(price,'.00'), '$') as int)),
	neighbourhood,
	bedrooms,
	review_scores_rating
from
	airbnb_listings
```


2. What neighborhoods seem to be the most popular?

Good ol' Williamsburg is the most popular hood.

```
select
	neighbourhood,
	count(*) as listings_count
from
	airbnb_listings
group by neighbourhood
order by listings_count desc
```


3. What time of year is the cheapest time to go to your city? What about the busiest?

```
I don't know how to gather this. I don't think we have timeseries data.
```