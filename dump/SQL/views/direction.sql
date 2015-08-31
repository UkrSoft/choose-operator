CREATE VIEW `direction` AS
    SELECT 
        dir.id AS dir_id,
        dir.name AS dir_name,
        dir.description AS dir_description,
        fl.loc_id AS from_location_id,
        fl.loc_name AS from_location_name,
        fl.loc_type_id AS from_location_type_id,
        fl.loc_type_name AS from_location_type_name,
        fl.loc_included_in_id AS from_location_included_in_id,
        tl.loc_id AS to_location_id,
        tl.loc_name AS to_location_name,
        tl.loc_type_id AS to_location_type_id,
        tl.loc_type_name AS to_location_type_name,
        tl.loc_included_in_id AS to_location_included_in_id,
        operator.*
    FROM
        bestoperator_direction dir
            LEFT JOIN
        location fl ON fl.loc_id = dir.from_location_id
            LEFT JOIN
        location tl ON tl.loc_id = dir.to_location_id
            LEFT JOIN
        bestoperator_direction_to_operator dto ON dto.direction_id = dir.id
            LEFT JOIN
        operator ON operator.operator_id = dto.operator_id;