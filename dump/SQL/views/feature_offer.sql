CREATE OR REPLACE VIEW `feature_offer` AS
    SELECT 
        f.*,
		ofr.*
    FROM
        feature f
		left join offer ofr on ofr.off_id = f.feature_offer_id;