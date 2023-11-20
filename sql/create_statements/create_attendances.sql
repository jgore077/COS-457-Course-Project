-- Table: vbms.attendance

-- DROP TABLE IF EXISTS vbms.attendance;

CREATE TABLE IF NOT EXISTS vbms.attendance
(
    practice_id integer NOT NULL,
    user_id integer NOT NULL,
    attendance_status integer,
    CONSTRAINT practice_pkey FOREIGN KEY (practice_id)
        REFERENCES vbms.practice (practice_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT user_fkey FOREIGN KEY (user_id)
        REFERENCES vbms.users (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        NOT VALID,
    CONSTRAINT status_check CHECK (attendance_status >= 0 AND attendance_status <= 2) NOT VALID
)

TABLESPACE pg_default;


COMMENT ON COLUMN vbms.attendance.attendance_status
    IS '0-absent, 1-present, 2-excused';
-- Index: fki_user_fkey

-- DROP INDEX IF EXISTS vbms.fki_user_fkey;

CREATE INDEX IF NOT EXISTS fki_user_fkey
    ON vbms.attendance USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;