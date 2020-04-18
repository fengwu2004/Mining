from typing import Dict
from data.codeInfo import CodeInfo

class BlockInfo(object):

    def __init__(self):

        super().__init__()

        self.name = ""

        self.codeList = []

    def createCodeList(self, dic:Dict):

        for item in dic:

            codeInfo = CodeInfo()

            codeInfo.code = item["code"]

            codeInfo.name = item["name"]

            self.codeList.append(codeInfo)
              
    def createFromJson(self, name:str, dic:Dict):

        self.name = name

        self.createCodeList(dic)

    def toJson(self):

        codeList = []

        for code in self.codeList:

            codeList.append({"name":code.name, "code":code.code})

        return {"name":self.name, "codeList":codeList}