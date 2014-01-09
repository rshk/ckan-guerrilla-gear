--select distinct "key" from package_extra order by "key"
--select distinct value from package_extra where key='Titolare'
--select maintainer, count(*) from package group by maintainer order by count desc

select distinct p.author, p.maintainer, g.name
from package p, "member" m, "group" g
where m.table_name = 'package'
and m.table_id = p.id
and g.id = m.group_id