import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo

class HandleCapitalInfo(RequestBaseManager):
    
    def post (self, *args, **kwargs):
        
        if self.checkToken() is not True:
            
            self.write({'success': -1})
    
            return

        data = json.loads(self.request.body.decode('utf-8'))
        
        allInfos = data['capitals']

        result = []

        for key in allInfos:

            value = allInfos[key]

            result.append({"code":key, "capital":value})

        DatabaseMgr.instance().capitals.remove({})

        DatabaseMgr.instance().capitals.insert_many(result)

        self.write({'success': 1})