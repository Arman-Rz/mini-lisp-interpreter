class VarTable():
    def __init__(self):
        self._varList = {}
    
    def SetVar(self, varName, varNode):
        self._varList[varName] = varNode
    
    def GetVar(self, varName):
        return self._varList.get(varName, None)
    
    def VarExists(self, varName):
        return varName in self._varList
    
    def GetAll(self):
        return self._varList