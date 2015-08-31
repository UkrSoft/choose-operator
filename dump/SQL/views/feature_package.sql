CREATE VIEW `feature_package` AS
    SELECT 
        f.*,
		pack.*
    FROM
        feature f
		left join `package` pack on pack.package_id = f.feature_package_id;