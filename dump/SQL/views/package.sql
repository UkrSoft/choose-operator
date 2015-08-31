CREATE OR REPLACE VIEW `package` AS
    SELECT 
        p.id AS package_id,
        p.name AS package_name,
        p.description AS package_description,
        p.price AS package_price,
        p.operator_id AS package_operator_id,
        p.link AS package_link,
		pt.id as package_type_id,
        pt.name AS package_type_name,
        term.*
    FROM
        bestoperator_package p
            LEFT JOIN
        bestoperator_packagetype pt ON pt.id = p.package_type_id
            LEFT JOIN
        po_term term ON term.term_id = p.po_term_id;