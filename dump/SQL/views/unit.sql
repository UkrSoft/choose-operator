CREATE VIEW `unit` AS
    SELECT 
        unit.id AS unit_id,
        unit.name AS unit_name,
        unit.compared_to_id AS unit_compared_to_id,
        unit.multiplier AS unit_multiplier
    FROM
        bestoperator_unit unit;