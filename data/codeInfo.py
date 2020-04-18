class CodeInfo(object):
    
    def __init__(self):

        super().__init__()

        self.name = ""

        self.code = ""

    def toJson(self):

        return {"name":self.name, "code":self.code}