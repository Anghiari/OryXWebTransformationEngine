'''
Created on Aug 27, 2013

@author: acer
'''

import smtplib
from constants import Constants

class MailService(object):
    '''
    This is the parent  mail service class
    '''

    SMTP_SERVER = None
    SMTP_PORT = None  
    sender = None
    recipient = None
    password = None

    def __init__(self):
        self.SMTP_SERVER = Constants.SMTP_SERVER
        self.SMTP_PORT = Constants.SMTP_PORT
        self.password = Constants.EMAIL_PWD
        self.sender = Constants.EMAIL_SENDER
    

    def sendEmail(self, subject, message, recipient):
        headers = ["From: " + self.sender,
           "Subject: " + subject,
           "To: " + recipient,
           "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        
        body = "" + message + ""
        
        
        session = smtplib.SMTP("smtp.gmail.com", self.SMTP_PORT)
     
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.sender, self.password)
         
        session.sendmail(self.sender, recipient, headers + "\r\n\r\n" + body)
        session.quit()