-- Table: vbms.announcements

-- DROP TABLE IF EXISTS vbms.announcements;

CREATE TABLE IF NOT EXISTS vbms.announcements
(
    announcement_id integer NOT NULL DEFAULT nextval('vbms.announcements_announcement_id_seq'::regclass),
    publisher_uid integer NOT NULL,
    date_published timestamp with time zone,
    content text COLLATE pg_catalog."default",
    CONSTRAINT annnouncements_pkey PRIMARY KEY (announcement_id),
    CONSTRAINT publisher_fkey FOREIGN KEY (publisher_uid)
        REFERENCES vbms.users (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        NOT VALID
)

TABLESPACE pg_default;
