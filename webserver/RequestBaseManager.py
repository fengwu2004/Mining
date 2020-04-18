import tornado.web
import json

class RequestBaseManager(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        
        self.set_header("Access-Control-Allow-Origin", "*")
        
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def checkToken(self):
        
        return True