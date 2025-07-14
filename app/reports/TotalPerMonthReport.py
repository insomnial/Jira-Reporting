from datetime import datetime
from dateutil.relativedelta import relativedelta

from reports.ReportBase import ReportBase

class TotalPerMonthReport(ReportBase):

    def getName(self) -> str:
        return "Total per month for previous 12 months"
    
    def __init__(self, FilterName, WorkItemList):
        super().__init__(FilterName=FilterName, WorkItems=WorkItemList)

    def generate(self) -> ReportBase:        
        self.ReportData['Name'] = f"{self.getName()}"
        self.ReportData['FilterName'] = self.FilterName
        data = {}
        for month in self.Range.keys():
            data[month] = len(self.Range[month])
        self.ReportData['Data'] = data
        return self
    