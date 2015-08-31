select
o.operator_id as oper_id
, o.operator_name as oper_name
, o.operator_link as oper_link
, p.package_id as pack_id
, p.package_name as pack_name
, p.package_description as pack_descr
, round(p.package_price, 0) as pack_price
, p.package_link as pack_link
, fp.feature_id as feature_package_id
, fp.feature_name as feature_package_name
, fp.pay_price as feature_package_price
, ofr.off_id as offer_id
, ofr.off_name as offer_name
, ofr.pay_price as offer_price
, fo.feature_id as offer_feature_id
, fo.feature_name as offer_feature_name
, fo.pay_price as offer_feature_price
from
operator o
join package p on p.package_operator_id = o.operator_id
left join feature_package fp on fp.feature_package_id = p.package_id
join offer ofr on ofr.off_package_id = p.package_id
left join feature_offer fo on fo.feature_offer_id = ofr.off_id
where /*TODO replace all names with corresponding IDs*/
o.loc_from_location_name = 'Україна' /*direction.from location*/
and o.loc_to_location_name = 'Україна' /*direction.to location*/
and fp.feature_service_type_name in ('Інтернет', 'Дзвінки') /*filter by service type for package' feature*/
and fo.feature_service_type_name in ('Інтернет', 'Дзвінки') /*filter by service type for offer' feature*/
and o.operator_name in ('life :)', 'МТС') /*filter by from_operator - applied only if some rows are returned*/
and toper.name in ('life :)', 'Київстар')
/*and nv(p.price, 0)+nv(pfp.price, 0)+nv(offp.price, 0)+nv(fp.price, 0) < 20*/
/*TODO we should order results by their relevance. So we need to provide sql results with such column.
Relevance column should be calculated for each item which is participating in comparizon and then
engine should make sum of the MOST OF these features which fits into specified price.
Then all such tuples should be ordered by their relevance (qty of service / price).
Good practice will be take into account some specific terms of usage for each row in result and order by its convenience too*/
order by 1, 2