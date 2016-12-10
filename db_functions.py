#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    db_functions.py
'''
import random
import string
import sys
import MySQLdb
import dbconn2


# Helper function for generating a random hash link
# Credit to http://stackoverflow.com/questions/16516280/how-to-generate-a-hashed-share-link-using-flask
def generateRandomString():
    charset = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(charset) for i in xrange(24))
    return random_str

def addToPollTable(conn,poll_name,link,email):
    # Inserting the new poll into the database
    sql = "INSERT INTO poll values (NULL,%s,%s,%s,CURDATE());"
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    row = curs.execute(sql, (poll_name,link,email))

# Helper function that connects to the database
def connectToDB(path_to_cnf, db_name):
    dsn = dbconn2.read_cnf(path_to_cnf)
    dsn['db'] = db_name
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
    sql = "INSERT INTO poll_options VALUES(%s, NULL,NULL, %s)"
    for time in times:
        if time != "":
            curs.execute(sql, (poll_id,time,))
        
# Database function to insert the locations
def insertLocationOptions(conn, poll_id, locations):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO poll_options VALUES(%s, NULL, %s,NULL)"
    for location in locations:
        if location != "":
            curs.execute(sql, (poll_id,location,))

# Returns all of the votes so far for a given poll
def returnVotesForPoll(conn, poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT location,given_time,response FROM responses inner join poll_options USING (oid) WHERE responses.poll_id=%s;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall()

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

# Helper function to get the oid given a poll_id and value
def getOIDGivenPollID(conn,poll_id,val):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT oid FROM poll_options WHERE poll_id = %s and location=%s OR given_time=%s";
    curs.execute(sql, (poll_id,val,val,))
    row = curs.fetchone()
    return row['oid']

# Updates the database with the responses given by a user
def updateResponsesGivenPollID(conn,poll_id,checked_times, checked_locations):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for time in checked_times:
        # Get the OID given a time
        oid = getOIDGivenPollID(conn,poll_id,time)
        sql = "INSERT INTO responses (poll_id, oid, response) VALUES(%s,%s,1) ON DUPLICATE KEY UPDATE response=response+1"
        curs.execute(sql, (poll_id,oid))

    for location in checked_locations:
        # Get the OID given a location
        oid = getOIDGivenPollID(conn,poll_id,location)
        sql2 = "INSERT INTO responses (poll_id,oid,response) VALUES(%s,%s,1) ON DUPLICATE KEY UPDATE response=response+1";
        curs.execute(sql2, (poll_id,oid))
