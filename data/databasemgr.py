from pymongo import MongoClient

_instance = None

_debug = False

class DatabaseMgr(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = DatabaseMgr()

        return _instance
    
    def __init__(self):

        uri = "mongodb://172.28.222.231:27017/recommond?"

        # uri = "mongodb://yanli:9394@123.206.230.152:27017/recommond?authMechanism=SCRAM-SHA-1"

        self.client = MongoClient(uri)

        # self.client = MongoClient()

        self.db = self.client["recommond"]

    @property
    def consultors(self):

        return self.db['consultors']
    
    @property
    def stocks(self):
        
        return self.db['stocks']

    @property
    def consultorLevels(self):

        return self.db['consultor_level']

    @property
    def stockLevels(self):

        return self.db['stock_level']

    @property
    def industry(self):

        return self.db['industry']

    @property
    def suggests(self):
        
        return self.db['suggest']

    @property
    def suggestscopy(self):
        
        return self.db['suggest_copy']

    @property
    def stockInfos(self):
        
        return self.db['stockinfo']

    def stockvolumof(self, dt:str):

        return self.db[dt]

    @property
    def selfselect(self):

        return self.db['selfselect']

    @property
    def users(self):
        
        return self.db['users']