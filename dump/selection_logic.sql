select
o.name as oper_name
, o.link as oper_link
, p.id as pack_id
, p.name as pack_name
, p.description as pack_descr
, round(p.price, 0) as pack_price
, p.link as pack_link
, pf.id as pack_feature_id
, ps.name as pack_service_name
, pst.name as pack_service_type
, off.name as offer_name
, s.name as service_name
, st.name as st_name from
bestoperator_operator o
join bestoperator_package p on p.operator_id = o.id
left join bestoperator_feature pf on pf.package_id = p.id
left join bestoperator_service ps on pf.service_id = ps.id
left join bestoperator_servicetype pst on pst.id = ps.service_type_id
left join bestoperator_offer_package oftp on oftp.package_id = p.id 
left join bestoperator_offer off on oftp.offer_id = off.id
left join bestoperator_feature f on f.offer_id = off.id
left join bestoperator_service s on f.service_id = s.id
left join bestoperator_servicetype st on st.id = s.service_type_id
left join bestoperator_direction d on s.direction_id = d.id
left join bestoperator_location fl on d.from_location_id = fl.id
left join bestoperator_location tl on d.to_location_id = tl.id
left join bestoperator_operator toper on toper.id = d.to_operator_id
left join bestoperator_payment pfp on pf.id = pfp.feature_id
left join bestoperator_payment offp on off.id = offp.offer_id
left join bestoperator_payment fp on f.id = fp.feature_id
where /*TODO replace all names with corresponding IDs*/
st.name in ('Інтернет', 'Дзвінки') /*filter by service type*/
and o.name in ('life :)', 'МТС') /*filter by from_operator - applied only if some rows are returned*/
and fl.name = 'Україна' /*direction.from location*/
and tl.name = 'Україна' /*direction.to location*/
and toper.name in ('life :)', 'Київстар') /*or use this when nothing is returned: toper.name = 'Інші'*/
/*and nval(p.price, 0)+nval(pfp.price, 0)+nval(offp.price, 0)+nval(fp.price, 0) < 20*/
order by o.name, p.name