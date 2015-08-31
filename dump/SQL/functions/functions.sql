DELIMITER //
DROP FUNCTION IF EXISTS nv//
create function nv (val integer, def_val integer)
returns int
	begin
	return case when val is null then def_val else val end;
	end//
DELIMITER ;