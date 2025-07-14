# place holder

import sqlite3
from tqdm.auto import tqdm
import json

from atlassian_api_py import controllerapi

from workitems.WorkItem import WorkItem

class WorkItemController:

    def __init__(self, aApiCon : controllerapi):
        super().__init__()
        self.KeyDict = {}
        self.ApiController = aApiCon
        self.FilterId = ''
        self.WorkItemDict = {}
        self.DbConn = None
        self.FilterName = ''

    ###########################################################################
    # Internal methods
    ###########################################################################
    
    # Gets the work items associated with the specified filter
    def _getWorkItemsUsingFilter(self) -> bool:
        print(f"# Get work items with filter: {self.FilterId}")
        getFilter = self.ApiController.get_filter(self.FilterId)
        self.FilterName = getFilter['name']
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

            # IF check if work item exists in DB and matches update time
            cursor = self.DbConn.cursor()
            query = cursor.execute(f'SELECT * FROM `workitem_detail` WHERE `key` = "{key}"').fetchone()
            if query != None and key == query[1]:
                # THEN load item details from DB, not network
                detailsDict = json.loads(query[11])
                workitem.saveDetails({
                    'id' : None,
                    'self' : None,
                    'names' : {v:v for v in detailsDict.keys()},
                    'fields' : detailsDict
                })
                pass
            else:
                # ELSE get item from network
                issueDetailsJson = self.ApiController.get_issue(issueIdOrKey=key, fieldsByKeys=True)
                workitem.saveDetails(issueDetailsJson)

                # get issue changelogs
                isLast = False
                startAt = 0
                changelogs = []
                while not isLast:
                    changelogJson = self.ApiController.get_changelogs(key)
                    isLast = changelogJson['isLast']
                    startAt = startAt + changelogJson['total']
                    changelogs = changelogs + changelogJson['values']
                workitem.set('changeLog', changelogs)

                # save details in db
                self._saveWorkItemToDb(workitem)


            self.WorkItemDict[key] = workitem
            pass # for

    def _saveWorkItemToDb(self, workitem : WorkItem):
        key = workitem.key
        assignee = (workitem.get('Assignee'))['displayName']
        reporter = (workitem.get('Reporter'))['displayName']
        summary = workitem.get('Summary')
        updated = workitem.get('Updated')
        priority = (workitem.get('Priority'))['name']
        status = (workitem.get('Status'))['name']
        created = workitem.get('Created')
        issue_type = ''
        request_type = (workitem.get('Request Type'))['requestType']['name']
        details = json.dumps(workitem.fieldDict, sort_keys=True)

        insertSql = f'INSERT INTO ' \
            f'`workitem_detail` (key,assignee,reporter,summary,updated,priority,' \
                                f'status,created,issue_type,request_type,details) ' \
                                f'VALUES (?,?,?,?,?,?,?,?,?,?,?)'
            # f'VALUES (Null,{key},{assignee},{reporter},{summary},{updated},{priority},' \
            #         f'{status},{created},{issue_type},{request_type},{details}'
        cursor = self.DbConn.cursor()
        cursor.execute(insertSql, (f'{key}',f'{assignee}',f'{reporter}',f'{summary}',f'{updated}',f'{priority}',f'{status}',f'{created}',f'{issue_type}',f'{request_type}',f'{details}'))
        self.DbConn.commit()
        cursor.close()

        pass


    ###########################################################################
    # Public methods
    ###########################################################################
    
    def loadFromFilter(self, aFilter : str):
        self.FilterId = aFilter
        self._getWorkItemsUsingFilter()
        self._getWorkItemByKey()

    def getWorkItems(self) -> list:
        return self.WorkItemDict
    
    def setDatabaseConnection(self, aConn : sqlite3.Connection):
        self.DbConn = aConn
