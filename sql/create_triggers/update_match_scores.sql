CREATE OR REPLACE FUNCTION vbms.update_match_scores()
RETURNS TRIGGER
LANGUAGE plpgsql

AS
$$
DECLARE
    total_sets INTEGER;
    usm_wins INTEGER;
    opponent_wins INTEGER;
BEGIN
    -- Get the total number of sets for the game
    SELECT COUNT(*) INTO total_sets
    FROM vbms.sets
    WHERE game_id = NEW.game_id;

    -- Get the number of sets won by USM
    SELECT COUNT(*) INTO usm_wins
    FROM vbms.sets
    WHERE game_id = NEW.game_id AND usm_score > opponent_score;

    -- Calculate the number of sets won by the opponent
    opponent_wins := total_sets - usm_wins;

    -- Update the match_scores in the games table
    UPDATE vbms.games
    SET match_score = usm_wins || ' - ' || opponent_wins
    WHERE game_id = NEW.game_id;

    RAISE NOTICE '% % % %', NEW.game_id, total_sets, usm_wins, opponent_wins;

    RETURN NULL;
END;
$$;


DROP TRIGGER IF EXISTS update_match_scores_trigger ON vbms.sets;

CREATE TRIGGER update_match_scores_trigger
AFTER INSERT
ON vbms.sets
FOR EACH ROW
EXECUTE FUNCTION vbms.update_match_scores();