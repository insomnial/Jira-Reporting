import abc
import os
import json

from workitems.WorkItem import WorkItem

REPORT_FOLDER = 'output'

class ReportBase:

    def __init__(self, FilterName : str, WorkItems : dict):
        super().__init__()
        self.WorkItems = WorkItems
        self.FilterName = FilterName
        self.ReportData = None
        if not os.path.exists(REPORT_FOLDER):
            os.mkdir(REPORT_FOLDER)

    @abc.abstractmethod
    def generate(self):
        pass

    @abc.abstractmethod
    def getName(self) -> str:
        return "unnamed"
    
    def save(self):
        print(f"# Report > Saving {self.getName()} - {self.FilterName}")
        assert self.ReportData is not None
        filepath = os.path.join(REPORT_FOLDER, f'{self.getName()} - {self.FilterName}.json')
        if os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, 'w') as f:
            f.write(json.dumps(self.ReportData, sort_keys=False, indent=2))
