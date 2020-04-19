from data.securities import Securities
from data.codeInfo import CodeInfo
from data.block import BlockInfo
from storemgr.storemgr import SecuritiesMgr
from typing import Dict, List
from storemgr.excel_mananger import ExcelMgr

_instance = None
class FindHotBlock(object):

    @classmethod
    def instance(cls):

        global _instance

        if _instance is None:

            _instance = FindHotBlock()

        return _instance

    def __init__(self):

        super().__init__()

        self.limitCount = 10

    def refreshHotBlocks(self):

        result:Dict[str, List[CodeInfo]] = dict()
    
        blockList = SecuritiesMgr.instance().blockList

        for block in blockList:

            for codeInfo in block.codeList:

                securities = SecuritiesMgr.instance().getSecurities(codeInfo)

                if securities == None:

                    continue

                limitCount = securities.getCountOfLimitUp(20190419)

                if limitCount < self.limitCount:

                    continue

                if result.get(block.name) == None:

                    result[block.name] = []
                
                result[block.name].append(codeInfo)
                
        self.storeToExcel(result)

    def storeToExcel(self, dic:Dict[str, List[CodeInfo]]): 

        excelMgr = ExcelMgr()

        for key in dic:
            
            values = [codeInfo.name for codeInfo in dic[key]]

            excelMgr.saveRow(title = key, values = values)

        name = "/Users/aliasyan/OneDrive/hot_block/hot_block_{0}.xlsx".format(self.limitCount)

        excelMgr.save(name)

FindHotBlock.instance().refreshHotBlocks()

print(FindHotBlock.instance().limitCount, "finish")

# result:Dict[str, List[CodeInfo]] = dict()

# codeInfo = CodeInfo()

# if result.get("sdk") == None:

#     result["sdk"] = []

# result["sdk"].append(codeInfo)

# print(result)

# items:List[int] = list()

# print(len(items))

# name = "hot_block_{0}.xlsx".format(100)

# print(name)

# codeInfo = CodeInfo()

# codeInfo.code = "300063"

# codeInfo.name = "天龙集团"

# sec = SecuritiesMgr.instance().getSecurities(codeInfo)

# sec.doSomeTest(20190415)
