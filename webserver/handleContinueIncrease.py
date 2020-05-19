import json
from webserver.RequestBaseManager import RequestBaseManager
from data.databasemgr import DatabaseMgr
from data.block import CodeInfo, BlockInfo
from strategy.find_continue_increase import FindContinueIncrease

class HandleContinueIncrease(RequestBaseManager):
    
    def post (self, *args, **kwargs):
        
        if self.checkToken() is not True:
            
            self.write({'success': -1})
    
            return

        # data = json.loads(self.request.body.decode('utf-8'))
        
        codeInfos = FindContinueIncrease.instance().refreshBlocks()

        result = list()

        for codeInfo in codeInfos:

            result.append(codeInfo.toJson())

        self.write({'success': 1, "data":{"codeInfos":result}})