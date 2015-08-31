CREATE OR REPLACE VIEW `payment` AS
    SELECT 
        pay.id AS pay_id,
        pay.name AS pay_name,
        pay.price AS pay_price,
        pay.period_id AS pay_period_id,
        pay.feature_id AS pay_feature_id,
        pay.offer_id AS pay_offer_id,
        pay.term_of_usage_id AS pay_term_of_usage_id,
        tou.*
    FROM
        bestoperator_payment pay
            LEFT JOIN
        term_of_usage tou ON tou.tou_id = pay.term_of_usage_id;