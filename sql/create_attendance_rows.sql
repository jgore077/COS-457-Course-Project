CREATE OR REPLACE FUNCTION vbms.add_attendance_rows()
RETURNS TRIGGER
LANGUAGE plpgsql

AS
$$
DECLARE
    uid INTEGER;
BEGIN
    -- Example SELECT statement (You will replace this with your actual logic)
    -- INSERT INTO vmbs.attendance(practice_id, user_id) 
    -- SELECT NEW.practice_id, user_id FROM vmbs.users;
	FOR uid IN SELECT user_id
	FROM vbms.users
	LOOP 
	INSERT INTO vbms.attendance(practice_id, user_id, attendance_status) VALUES ( NEW.practice_id,uid, 0);
	RAISE NOTICE '% %', NEW.practice_id,uid;
	END LOOP;
	
	RETURN NULL;
    
    
END;
$$;

-- Make sure to use the correct schema name here, it should be vmbs (not vbms or vmbs)
DROP TRIGGER IF EXISTS add_attendance_rows_trigger ON vbms.practice;

CREATE TRIGGER add_attendance_rows_trigger
AFTER INSERT
ON vbms.practice
FOR EACH ROW
EXECUTE FUNCTION vbms.add_attendance_rows();