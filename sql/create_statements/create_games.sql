-- Table: vbms.games

-- DROP TABLE IF EXISTS vbms.games;

CREATE TABLE IF NOT EXISTS vbms.games
(
    game_id integer NOT NULL DEFAULT nextval('vbms.games_gid_seq'::regclass),
    location text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    gamedate timestamp without time zone NOT NULL,
    opponent text COLLATE pg_catalog."default",
    game_score text COLLATE pg_catalog."default",
    CONSTRAINT games_pkey PRIMARY KEY (game_id)
)

TABLESPACE pg_default;

