from datetime import datetime
from dateutil.relativedelta import relativedelta

from reports.ReportBase import ReportBase

class TimeToResolutionAverageReport(ReportBase):

    def getName(self) -> str:
        return "Average Time to Resolution for previous 12 months"
    
    def __init__(self, FilterName, WorkItemList):
        super().__init__(FilterName=FilterName, WorkItems=WorkItemList)

    def formatTimeFromMillisToMinutes(self, duration) -> str:
        seconds = duration // 1000
        minutes = seconds // 60
        return f'{minutes}m {seconds - (minutes * 60)}s'

    def generate(self) -> ReportBase:
        # copy month keys into results array
        self.Results = {}
        self.keyLabel = 'IT Time to Resolution'
        for month in self.Range:
            workitemsArray = self.Range[month]
            workitemcount = 0
            totalresponsetime = 0
            for wi in workitemsArray:
                tempDict = wi.get(self.keyLabel)
                if not wi.get(self.keyLabel): continue # skip work items with no ttfr saved
                try:
                    tempDict = tempDict['completedCycles'][0]
                except IndexError:
                    continue
                workitemcount += 1
                ttfrValue = tempDict['elapsedTime']['millis']
                totalresponsetime = ttfrValue
                pass
            if workitemcount == 0:
                avgTimeInMillis = 0
            else:
                avgTimeInMillis = totalresponsetime // workitemcount
            self.Results[month] = self.formatTimeFromMillisToMinutes(avgTimeInMillis)

        # saving report data in JSON format
        self.ReportData['Name'] = f"{self.getName()}"
        self.ReportData['Filter Name'] = self.FilterName
        self.ReportData['Key Label'] = self.keyLabel
        data = {}
        for month in self.Results.keys():
            data[month] = self.Results[month] if self.Results[month] != '0m 0s' else None
        self.ReportData['Data'] = data
        return self
    