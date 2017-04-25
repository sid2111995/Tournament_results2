DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;



--table game for handling games/matches
CREATE TABLE game(
    m_id SERIAL PRIMARY KEY,
    winner INTEGER,
    loser INTEGER
);


--table player for creating list of players

CREATE TABLE player(
    p_id SERIAL PRIMARY KEY,
    name TEXT
); 



CREATE VIEW rank AS SELECT p_id,name, (SELECT count(*) FROM game WHERE player.p_id = game.winner) AS wins, (SELECT count(*) FROM game WHERE player.p_id IN (game.loser,game.winner)) AS played FROM player ORDER BY wins DESC;
