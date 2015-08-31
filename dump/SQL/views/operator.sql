CREATE VIEW `operator` AS
    SELECT 
        o.id AS operator_id,
        o.name AS operator_name,
        o.description AS operator_description,
        o.link AS operator_link,
        l.loc_id AS operator_location_id,
        l.loc_name AS operator_location_name,
        l.loc_type_id AS operator_location_type_id,
        l.loc_type_name AS operator_location_type_name,
        l.loc_included_in_id AS operator_location_included_in_id
    FROM
        bestoperator_operator o
            LEFT JOIN
        location l ON o.location_id = l.loc_id;