from datetime import datetime
from dateutil.relativedelta import relativedelta

from reports.ReportBase import ReportBase

class UNIQUENAMEReport(ReportBase):

    def getName(self) -> str:
        return " for previous 12 months"
    
    def __init__(self, FilterName, WorkItemList):
        super().__init__(FilterName=FilterName, WorkItems=WorkItemList)
        # set up range for month-to-month captures
        self.ReportData = {}
        currentMonth = datetime.now()
        self.Range = {}
        for i in range(0, 11):
            self.Range[(datetime.today() + relativedelta(months=-i)).strftime('%B %Y')] = []

    def generate(self) -> ReportBase:
        # do things for report
         
        # saving report data in JSON format
        self.ReportData['Name'] = f"{self.getName()}"
        self.ReportData['Filter Name'] = self.FilterName
        data = {}
        for month in self.Range.keys():
            data[month] = len(self.Range[month])
        self.ReportData['Data'] = data
        return self
    