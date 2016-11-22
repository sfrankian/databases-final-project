#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    db_functions.py
'''
import sys
import MySQLdb
import dbconn2


# helper function that connects to the database
def connectToDB():
    dsn = dbconn2.read_cnf('~/.my.cnf')
    dsn['db'] = 'sfrankia_db'
    conn = dbconn2.connect(dsn)
    return conn

# Returns all of the time options associated with a given poll id
def getTimesByPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM poll_options WHERE poll_id = ? and given_time not NULL;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall() # returns all of the rows that match the sql query
# Returns all of the location options for a given poll id
def getLocationsByPollID(conn,poll_id):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM poll_options WHERE poll_id = ? and location not NULL;"
    curs.execute(sql, (poll_id,))
    return curs.fetchall() # returns all of the rows that match the sql query
