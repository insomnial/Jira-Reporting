class WorkItem:

    def __init__(self, aKeyId : str):
        super().__init__()
        self.key = aKeyId
        self.fieldMap = {}
        self.fieldDict = {}


    ###########################################################################
    # Setters
    ###########################################################################

    def saveDetails(self, aJsonDict : dict):
        self.id = aJsonDict['id']
        self.url = aJsonDict['self']
        self.fieldMap = aJsonDict['names']
        # filter out empty custom_field
        self.fieldDict = {self.fieldMap[k]:v for k,v in aJsonDict['fields'].items() if v}

    def set(self, aKey, aValue) -> bool:
        self.fieldDict[aKey] = aValue
        return True            

    ###########################################################################
    # Getters
    ###########################################################################

    def getWorkItemObject(self):
        return self
    
    def getFieldLabels(self) -> list:
        return [self.fieldDict.keys()]
    
    def get(self, aKey) -> str:
        if aKey in self.fieldDict.keys():
            return self.fieldDict[aKey]
        else:
            return None