CREATE VIEW `param` AS
    SELECT 
        attr.name AS param_name,
        unit.*,
        param.value AS param_value,
        param.feature_id AS param_feature_id
    FROM
        bestoperator_attribute attr
            LEFT JOIN
        bestoperator_param param ON param.attr_id = attr.id
            LEFT JOIN
        unit ON unit.unit_id = attr.unit_id;