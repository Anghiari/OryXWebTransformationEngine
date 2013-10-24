'''
Created on Jul 10, 2013

@author: acer
'''
import tornado
import constants.Constants as const
from database.DatabaseAdapter import DatabaseAdapter
session = None


class HomeHandler(tornado.web.RequestHandler):
    '''
        This Handler is just for the home page interface
    '''
    database = DatabaseAdapter.Instance()
    

    def get(self):
                # Initial setup of cookie
                
        if not self.get_secure_cookie(const.sessionID):
            app_id = self.get_argument("app_id", default=None, strip=False)
        
            if app_id is None:
                self.write("No authentication ID")
                return
            if(not self.authenticate(app_id)):
                self.write("App ID not authentic!" + app_id)
                return
        # Do authentication at this point
        # if authenticated, do this
            session = Session(app_id)
            self.set_secure_cookie(const.sessionID,str(session.session_id), expires_days= None)
            self.write(str(Session(app_id).session_id))
        self.render("proxy.html")
        
    def authenticate(self, app_id):
        return self.database.isInSystem(app_id)
        
class SessionHandler(tornado.web.RequestHandler):
 
    def get(self):
        self.write("clearing this cookie :" + str(self.get_cookie(const.sessionID)))
        self.clear_cookie(const.sessionID)
        
import uuid

class Session():

        
    app_id = None
    session_id = None
    
    def __init__(self, app_id):
        self.app_id = app_id
        self.session_id = uuid.uuid4()
