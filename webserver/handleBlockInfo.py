import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo

class HandleBlockInfo(RequestBaseManager):
    
    def post (self, *args, **kwargs):
        
        if self.checkToken() is not True:
            
            self.write({'success': -1})
    
            return

        data = json.loads(self.request.body.decode('utf-8'))
        
        allblocks = data['blocks']

        result = []

        for key in allblocks:

            blockInfo = BlockInfo()

            blockInfo.createFromJson(key, allblocks[key])

            result.append(blockInfo.toJson())

        DatabaseMgr.instance().block.remove({})

        DatabaseMgr.instance().block.insert_many(result)

        self.write({'success': 1})