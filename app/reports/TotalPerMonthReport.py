from datetime import datetime
from dateutil.relativedelta import relativedelta

from reports.ReportBase import ReportBase

class TotalPerMonthReport(ReportBase):

    def getName(self) -> str:
        return "Total number of WORK ITEM per month for past 12 months"
    
    def __init__(self, WorkItemList):
        super().__init__(WorkItems=WorkItemList)
        self.ReportData = {}
        currentMonth = datetime.now()
        self.Range = {}
        for i in range(0, 11):
            self.Range[(datetime.today() + relativedelta(months=-i)).strftime('%B %Y')] = []

        pass

    def generate(self) -> ReportBase:
        # given self.Range (list of "Month Year")
        # populate self.Range with 'July 2025' = [ITDESK-1, ITDESK-2, etc]
        for workitem in self.WorkItems.values():
            createdString = workitem.get('Created')
            if not createdString: continue # sanity check for created field existing
            createdString = createdString[:7] # cut off everything after YYYY-MM
            createdSearchString = datetime.strptime(createdString, '%Y-%m').strftime('%B %Y')
            if createdSearchString in self.Range.keys(): # if work item is created in our range, save it to the month
                tempArr = self.Range[createdSearchString]
                tempArr.append(workitem)
                self.Range[createdSearchString] = tempArr
        
        self.ReportData['Name'] = self.getName()
        data = {}
        for month in self.Range.keys():
            data[month] = len(self.Range[month])
        self.ReportData['Data'] = data
        return self
    