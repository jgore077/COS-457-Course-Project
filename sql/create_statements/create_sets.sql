-- Table: vbms.sets

-- DROP TABLE IF EXISTS vbms.sets;

CREATE TABLE IF NOT EXISTS vbms.sets
(
    game_id integer NOT NULL,
    set_num integer,
    usm_score integer,
    opponent_score integer,
    CONSTRAINT "game_idFK" FOREIGN KEY (game_id)
        REFERENCES vbms.games (game_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

