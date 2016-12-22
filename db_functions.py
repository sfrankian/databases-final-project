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

def addToPollTable(conn,poll_name,link,email,end_date):
    # Inserting the new poll into the database
    sql = "INSERT INTO poll values (NULL,%s,%s,%s,CURDATE(),%s);"
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    row = curs.execute(sql, (poll_name,link,email,end_date,))

# Helper function that connects to the database
def connectToDB(path_to_cnf, db_name):
    dsn = dbconn2.read_cnf(path_to_cnf)
    dsn['db'] = db_name
    conn = dbconn2.connect(dsn)
    return conn

# Returns all of the time options associated with a given poll id
def getOptionsByPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT oid,meeting_date,given_time,location FROM poll_options WHERE poll_id = %s;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall() # returns all of the rows that match the sql query

# Database function to insert the locations into poll options
def insertOptions(conn, poll_id, options):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO poll_options VALUES(%s, NULL,%s, %s,%s)"

    for option in options:
        curs.execute(sql, (poll_id,option[0],option[1],option[2],))
        
# Returns all of the votes so far for a given poll
def returnVotesForPoll(conn, poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT location,given_time,meeting_date,response FROM responses inner join poll_options USING (oid) WHERE responses.poll_id=%s;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall()

# Returns a poll's ID given a hashed link
def getPollIDGivenLink(conn, link):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT id FROM poll WHERE link = %s"
    curs.execute(sql, (link,))
    row = curs.fetchone()
    return row['id']


# Helper function to get the oid given a poll_id and value
def getOIDGivenPollID(conn,poll_id,option):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT oid FROM poll_options WHERE poll_id = %s and given_time=%s";
    curs.execute(sql, (poll_id,option,))
    row = curs.fetchone()
    return row['oid']

# Updates the database with the responses given by a user
def updateResponsesGivenPollID(conn,poll_id,checked_options):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for option in checked_options:
        # Get the OID given a time
        sql = "INSERT INTO responses (poll_id, oid, response) VALUES(%s,%s,1) ON DUPLICATE KEY UPDATE response=response+1"
        curs.execute(sql, (poll_id,option,))
   
# Returns a dictionary containing the ids and emails of all the polls expiring today
def getPollsExpiringToday(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT id,email FROM poll where expire_date = CURDATE();"
    curs.execute(sql)
    return curs.fetchall()

# Returns a dictionary containing the ids and emails of all the polls expiring today
def getPollsExpiredYesterday(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT id,email FROM poll where expire_date = SUBDATE(CURDATE(),1);"
    curs.execute(sql)
    return curs.fetchall()

def getEmailAddressGivenPollID(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT id FROM poll where expire_date = CURDATE();"
    curs.execute(sql)
    return curs.fetchall()
