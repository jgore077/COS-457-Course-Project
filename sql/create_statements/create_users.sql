

--DROP TABLE IF EXISTS vbms.users;

CREATE TABLE IF NOT EXISTS vbms.users
(
    user_id integer NOT NULL DEFAULT nextval('vbms.users_uid_seq'::regclass),
    email text COLLATE pg_catalog."default",
    uname text COLLATE pg_catalog."default",
    pword text COLLATE pg_catalog."default",
    role text COLLATE pg_catalog."default",
    phone_num text COLLATE pg_catalog."default",
    is_commuter boolean,
    shirt_size text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

