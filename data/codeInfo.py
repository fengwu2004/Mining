class CodeInfo(object):

    def __init__(self, code="", name=""):

        super().__init__()

        self.name = name

        self.code = code

    def __eq__(self, value):

        return self.code == value.code

    def toJson(self):

        return {"name":self.name, "code":self.code}