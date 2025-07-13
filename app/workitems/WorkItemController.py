# place holder

import sqlite3
from tqdm.auto import tqdm

from atlassian_api_py import controllerapi

from workitems.WorkItem import WorkItem

class WorkItemController:

    def __init__(self, aApiCon : controllerapi):
        super().__init__()
        self.KeyDict = {}
        self.ApiController = aApiCon
        self.FilterId = ""
        self.WorkItemDict = {}

    
    # Gets the work items associated with the specified filter
    def _getWorkItemsUsingFilter(self) -> bool:
        print(f"# Get work items with filter: {self.FilterId}")
        getFilter = self.ApiController.get_filter(self.FilterId)
        filterSql = getFilter['jql']
        isLast = False
        nextPageToken = ''
        keyList = []
        while not isLast:
            search = self.ApiController.search_jql(aJql=filterSql, nextPageToken=nextPageToken, maxResults=1000)
            if 'isLast' in search: isLast = search['isLast']
            if 'nextPageToken' in search: nextPageToken = search['nextPageToken']
            issues = search['issues']
            for item in issues:
                key = item['key']
                keyList.append(key)
        self.KeyDict['keyList'] = keyList
        print(f"Work items found: {len(keyList)}")
        return True

    # Gets work item details using list of key IDs
    def _getWorkItemByKey(self) -> bool:
        print(f"# Get work item details")
        for key in tqdm(self.KeyDict['keyList']):
            # print(f"# {key}")
            # print(f"  - Get issue details")

            workitem = WorkItem(aKeyId=key)

            # get issue details
            issueDetailsJson = self.ApiController.get_issue(issueIdOrKey=key, fieldsByKeys=True)

            # save details in work item
            workitem.saveDetails(issueDetailsJson)

            # TODO Get issues details: assignee, status, created date, updated date

            # get issue changelogs
            # print(f"  - Get issue changelogs")
            isLast = False
            startAt = 0
            changelogs = []
            while not isLast:
                changelogJson = self.ApiController.get_changelogs(key)
                isLast = changelogJson['isLast']
                startAt = startAt + changelogJson['total']
                changelogs = changelogs + changelogJson['values']
                pass # while
            workitem.set('changeLog', changelogs)

            self.WorkItemDict[key] = workitem

            pass # for


    def loadFromFilter(self, aFilter : str):
        self.FilterId = aFilter
        self._getWorkItemsUsingFilter()
        self._getWorkItemByKey()

    def getWorkItems(self) -> dict:
        return self.WorkItemDict