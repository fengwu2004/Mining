class CodeInfo(object):
    
    def __init__(self):

        super().__init__()

        self.name = ""

        self.code = ""  

    def __eq__(self, value):

        return self.code == value.code

    def toJson(self):

        return {"name":self.name, "code":self.code}