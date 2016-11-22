#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    db_functions.py
'''
import random
import string
from hashlib import sha512
import MySQLdb
import dbconn2


# Helper function for generating a random hash link
# Credit to http://stackoverflow.com/questions/16516280/how-to-generate-a-hashed-share-link-using-flask
def generateRandomString():
    charset = string.ascii_letter + string.digits
    return ''.join(random.choice(charset) for i in xrange(24))

# Returns a random hashed link given a poll id and updates the database entry to
# include the generated hash
# Credit to http://stackoverflow.com/questions/16516280/how-to-generate-a-hashed-share-link-using-flask
def generateAndStoreHash(conn, poll_id):
    # generating the hash
    hash = sha512()
    hash.update(generateRandomString())
    myhash = hash.hexdigest()[:24]
    
    # Updating the database
    sql = "UPDATE poll SET link=%s WHERE id=%s"
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    row = curs.execute(sql, (myhash,poll_id,))

    return myhash
    
# Helper function that connects to the database
def connectToDB():
    dsn = dbconn2.read_cnf('/students/sfrankia/.my.cnf')
    dsn['db'] = 'sfrankia_db'
    conn = dbconn2.connect(dsn)
    return conn

# Returns all of the time options associated with a given poll id
def getTimesByPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM poll_options WHERE poll_id = %s and given_time not NULL;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall() # returns all of the rows that match the sql query
# Returns all of the location options for a given poll id
def getLocationsByPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM poll_options WHERE poll_id = %s and location not NULL;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall() # returns all of the rows that match the sql query
