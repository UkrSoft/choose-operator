CREATE OR REPLACE VIEW `location` AS
    SELECT 
        loc.id AS loc_id,
        loc.name AS loc_name,
        loc.included_in_id AS loc_included_in_id,
        loc.location_type_id AS loc_type_id,
        loct.name AS loc_type_name
    FROM
        bestoperator_location AS loc
            LEFT JOIN
        bestoperator_locationtype AS loct ON loct.id = loc.location_type_id;