CREATE OR REPLACE VIEW `offer` AS
    SELECT 
        off.id AS off_id,
        off.name AS off_name,
        off.link AS off_link,
        pay.*,
        po_term.*,
        offp.package_id AS off_package_id
    FROM
        bestoperator_offer off
            LEFT JOIN
        payment pay ON pay.pay_offer_id = off.id
            LEFT JOIN
        po_term ON po_term.term_id = off.po_term_id
            LEFT JOIN
        bestoperator_offer_package offp ON offp.offer_id = off.id;