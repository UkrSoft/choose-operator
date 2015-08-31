CREATE VIEW `term_of_usage` AS
    SELECT 
        tou.id AS tou_id,
        tou.name AS tou_name,
        tou.amount AS tou_amount,
        tou.unit_id AS tou_unit_id,
        unit.name AS tou_unit_name,
        tou.criterion_id AS tou_criterion_id,
        crit.name AS tou_criterion_name
    FROM
        bestoperator_termofusage tou
            LEFT JOIN
        bestoperator_unit unit ON unit.id = tou.unit_id
            LEFT JOIN
        bestoperator_criterion crit ON crit.id = tou.criterion_id;