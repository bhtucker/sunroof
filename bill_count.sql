
-- Please include a list of all legislators that used this term, the number of their bills that used this term, and sort all results by this bill count.

select 
	concat(l.first_name, ' ', l.last_name), count(b.bill_id)
	from bills b join legislators l
	on b.sponsor_id = l.bioguide_id
group by concat(l.first_name, ' ', l.last_name)
order by count(b.bill_id) DESC;
