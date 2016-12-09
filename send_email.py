#!/usr/local/bin/python2.7

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendPollCreatedEmail(email_addr, poll_link):
    msg_body = "This is an automated message generated by WhenAndWhere.\n"
    msg_body += "You can access your poll here: \ncs.wellesley.edu:9874/poll_response/" + poll_link 
    msg_body += "\nand the responses to your poll at cs.wellesley.edu:9874/view_responses/" + poll_link

    msg = MIMEMultipart()
    msg['From'] = 'sfrankia@tempest.wellesley.edu'
    msg['To'] = email_addr
    msg['Subject'] = 'Your WhenAndWhere Poll'
    
    msg.attach(MIMEText(msg_body,'plain'))
    server = smtplib.SMTP('localhost')
    server.sendmail('sfrankia@tempest.wellesley.edu',email_addr,msg.as_string())
    server.quit()
