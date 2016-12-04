#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    db_functions.py
'''
import random
import string
import sys
from hashlib import sha512
import MySQLdb
import dbconn2


# Helper function for generating a random hash link
# Credit to http://stackoverflow.com/questions/16516280/how-to-generate-a-hashed-share-link-using-flask
def generateRandomString():
    charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for i in xrange(24))

# Returns a random hashed link given a poll id and updates the database entry to
# include the generated hash
# Credit to http://stackoverflow.com/questions/16516280/how-to-generate-a-hashed-share-link-using-flask
def generateAndStoreHash(conn):
    # generating the hash
    hash = sha512()
    hash.update(generateRandomString())
    myhash = hash.hexdigest()[:24]

    
    # Inserting the new poll with its hash into the database
    sql = "INSERT INTO poll values(NULL,'hi',%s,CURDATE())"
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    row = curs.execute(sql, (myhash,))

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


# Database function to insert the locations into poll options
def insertTimeOptions(conn, poll_id, times):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO poll_options VALUES(NULL, %s,NULL, %s)"
    for time in times:
        if time != "":
            curs.execute(sql, (poll_id,time,))
        
# Database function to insert the locations
def insertLocationOptions(conn, poll_id, locations):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO poll_options VALUES(NULL, %s, %s,NULL)"
    for location in locations:
        if location != "":
            curs.execute(sql, (poll_id,location,))

# Returns a poll's ID given a hashed link
def getPollIDGivenLink(conn, link):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT id FROM poll WHERE link = %s"
    curs.execute(sql, (link,))
    row = curs.fetchone()
    return row['id']

# Returns all of the time poll options associated with a poll ID
def getTimesGivenPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT given_time FROM poll_options WHERE poll_id = %s and given_time is not NULL";
    curs.execute(sql, (poll_id,))
    return curs.fetchall()

# Returns all of the location poll options associated with a poll ID
def getLocationsGivenPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT location FROM poll_options WHERE poll_id = %s and location is not NULL";
    curs.execute(sql, (poll_id,))
    return curs.fetchall()
