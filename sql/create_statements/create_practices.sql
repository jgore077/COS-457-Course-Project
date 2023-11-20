
CREATE TABLE IF NOT EXISTS vbms.practice
(
    practice_id integer NOT NULL DEFAULT nextval('vbms."practice _practice_id_seq"'::regclass),
    description text COLLATE pg_catalog."default",
    location text COLLATE pg_catalog."default",
    date timestamp with time zone,
    CONSTRAINT practice_pkey PRIMARY KEY (practice_id)
)

TABLESPACE pg_default;
