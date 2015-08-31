CREATE VIEW `po_term` AS
    SELECT 
        term.id AS term_id,
        term.name AS term_name,
        term.is_active AS term_active,
        term.active_from_date AS term_active_from_date,
        term.active_to_date AS term_active_to_date,
        term.order_from_date AS term_order_from_date,
        term.order_to_date AS term_order_to_date
    FROM
        bestoperator_poterm term;