CREATE OR REPLACE VIEW `feature` AS
    SELECT 
        fea.id AS feature_id,
        fea.name AS feature_name,
        fea.offer_id AS feature_offer_id,
        fea.package_id AS feature_package_id,
        service.*,
		pay.*
    FROM
        bestoperator_feature fea
            LEFT JOIN
        service ON service.service_id = fea.service_id
		    LEFT JOIN
		payment pay on pay.pay_feature_id = fea.id;