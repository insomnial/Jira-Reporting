import abc
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from workitems.WorkItem import WorkItem

REPORT_FOLDER_BASE = 'output'

class ReportBase:

    def __init__(self, FilterName : str, WorkItems : dict):
        super().__init__()
        self.WorkItems = WorkItems
        self.FilterName = FilterName
        self.ReportData = {}
        currentMonth = datetime.now()
        self.Range = {}
        self._splitWorkItemsIntoMonths()
        self.ReportPath = os.path.join(REPORT_FOLDER_BASE, FilterName)
        if not os.path.exists(self.ReportPath):
            os.mkdir(self.ReportPath)

    @abc.abstractmethod
    def generate(self):
        pass

    @abc.abstractmethod
    def getName(self) -> str:
        return "unnamed"
    
    def _splitWorkItemsIntoMonths(self):
        # create previous 12 months array
        for i in range(0, 11):
            self.Range[(datetime.today() + relativedelta(months=-i)).strftime('%B %Y')] = []

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
    
    def save(self):
        print(f"# Report > Saving {self.FilterName}/{self.getName()}")
        assert self.ReportData is not None
        filepath = os.path.join(self.ReportPath, f'{self.getName()}.json')
        if os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, 'w') as f:
            f.write(json.dumps(self.ReportData, sort_keys=False, indent=2))
