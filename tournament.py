#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    
    try:
        dataname = 'tournament'
        db = psycopg2.connect("dbname={}".format(dataname))
        cursor = db.cursor()
        return db, cursor
    except:
        print("error in process!!")

def deleteMatches():
    """Remove all the match records from the database."""
    db,cursor = connect()
    query = "TRUNCATE " + 'game'
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    db,cursor = connect()
    query = "TRUNCATE " + 'player'
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    

def countPlayers():
    """Returns the number of players currently registered."""
    db,cursor = connect()
    query = "SELECT count(*) FROM player"
    cursor.execute(query)
    val = cursor.fetchall()
    cursor.close()
    db.close()
    return int(val[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    if name:
        query = "INSERT into player(name) values(%s)"
        db, cursor = connect()
        cursor.execute(query, (name, ))
        db.commit()
        cursor.close()
        db.close()
    else:
        return false

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT p_id, name , wins, played FROM rank"
    db,cursor = connect()
    cursor.execute(query)
    val = cursor.fetchall()
    cursor.close()
    db.close()
    return val

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO game(winner, loser) VALUES (%s,%s)"
    cursor.execute(query, (winner,loser))
    db.commit()
    db.close()




def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    """
    db, cursor = connect()
    pairs = []
    total = countPlayers()
    for p in xrange(0, total, 2):
        q = """SELECT p_id, name FROM rank ORDER BY wins
        LIMIT 2 OFFSET """ + str(p)
        cursor.execute(q)
        res = cursor.fetchall()
        res = res[0] + res[1]
        pairs.append(res)
    return pairs


