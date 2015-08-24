DELIMITER //
DROP FUNCTION IF EXISTS nval//
create function nval (val integer, def_val integer)
returns int
	begin
	return case when val is null then def_val else val end;
	end//
DELIMITER ;