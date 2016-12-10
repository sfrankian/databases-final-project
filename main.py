#!/usr/local/bin/python2.7

''' Stephanie Frankian and Elizabeth Kuszmaul
    November 22, 2016
    main.py
'''
import db_functions
import send_email
import sys
from flask import Flask, request,render_template, redirect, url_for, make_response

path_to_cnf = sys.argv[1]
db_name = sys.argv[2]
conn = db_functions.connectToDB(path_to_cnf,db_name) # saving the conn so we don't need to reconnect with every query
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/process/', methods=["GET","POST"])
def process():
    if request.method == "POST":
        # Making the hashed link and storing it in the database
        email = request.form["email"]
        poll_name = request.form["name"]
        myhash = db_functions.generateRandomString()
        db_functions.addToPollTable(conn,poll_name,myhash,email)
        times = []
        locations = []
        
        for key in request.form.keys():
            if key[:4] == "time":
                times.append(request.form[key])
            elif key[:8] == "location":
                locations.append(request.form[key])
                
        # Get the poll_id for a given link
        poll_id = db_functions.getPollIDGivenLink(conn, myhash)
        
        # Database function to insert the locations into poll options
        db_functions.insertTimeOptions(conn,poll_id,times)
        
        # Database function to insert the locations
        db_functions.insertLocationOptions(conn,poll_id,locations)

        # Send link to the poll creator
        send_email.sendPollCreatedEmail(email,myhash)
        return render_template( 'thanks_for_creating_poll.html', poll_name=poll_name,myhash=myhash)
    
@app.route('/poll_response/<myhash>', methods=["GET","POST"])
def poll_response(myhash):
    if request.method == "POST":
        return redirect( url_for('thanks') )
    else:
        pollanswered = request.cookies.get(myhash)
        if pollanswered:
            return redirect(url_for('already_voted'))
        else:
            poll_id = db_functions.getPollIDGivenLink(conn, myhash) # getting the proper poll_id
            times = db_functions.getTimesGivenPollID(conn,poll_id)
            locations = db_functions.getLocationsGivenPollID(conn,poll_id)
            resp = make_response( render_template("poll_response.html",script=url_for('process_response',myhash=myhash),locations=locations,times=times))
            resp.set_cookie(myhash, 'submitted response')
            return resp

@app.route('/process_response/<myhash>', methods=["GET", "POST"])
def process_response(myhash):

    if request.method == "POST":
        # Getting the checked boxes from the form
        checked_times = request.form.getlist('time')
        checked_locations = request.form.getlist('location')
		
        # TODO: votes to the database to update
        poll_id = db_functions.getPollIDGivenLink(conn, myhash) # getting the proper poll_id
        db_functions.updateResponsesGivenPollID(conn,poll_id,checked_times, checked_locations)		
        # Updating the database with the checked responses
        return redirect(url_for('thanks'))


		
@app.route('/view_responses/<myhash>', methods=["GET","POST"])
def view_responses(myhash):
    poll_id = db_functions.getPollIDGivenLink(conn, myhash) # getting the proper poll_id
    responses_dict = db_functions.returnVotesForPoll(conn,poll_id)
    return render_template("view_responses.html", responses_dict=responses_dict)

@app.route('/thanks/', methods=["GET","POST"])
def thanks():
    return render_template("thanks.html")

@app.route('/already_voted/', methods=["GET","POST"])
def already_voted():
    return render_template("already_voted.html")

@app.route('/create/', methods = ["GET","POST"])
def create():
    return render_template("create.html", meth='POST',script=url_for('process'))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9876)


