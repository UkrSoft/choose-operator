CREATE VIEW `service` AS
    SELECT 
        service.id AS service_id,
        service.name AS service_name,
        service.service_type_id AS service_type_id,
        st.name AS service_type_name,
        st.is_displayed AS service_type_is_displayed,
        direction.*
    FROM
        bestoperator_service service
            LEFT JOIN
        bestoperator_servicetype st ON st.id = service.service_type_id
            LEFT JOIN
        direction ON direction.dir_id = service.direction_id;