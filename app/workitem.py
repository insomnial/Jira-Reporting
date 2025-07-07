import sqlite3

class WorkItem:
    DbConn = None
    DetailFields = None
    FieldMap = None
    ChangeLogList = None
    AtlassianKey = None
    SqlTables = None

    def __init__(self, aDbConn : sqlite3.Connection):
        # TODO move all this to controllerdb.py
        # query tables and get column names
        global DbConn
        global SqlTables

        DbConn = aDbConn
        SqlTables = {}

        cursor = DbConn.execute('select * from layout')
        # store table names in db
        for row in cursor.fetchall():
            SqlTables[row[1]] = []
        # store column names for each table in db
        for table in SqlTables.keys():
            cursor = DbConn.execute(f'select * from `{table}` limit 1')
            names = [description[0] for description in cursor.description]
            SqlTables[table] = names

    # container for work items
    # def __init__(self, itemDict : dict, fieldMap):
    #     self.fieldMap = fieldMap
    #     self.assignee = itemDict['assignee']
    #     self.reporter = itemDict['reporter']
    #     self.summary = itemDict['summary']
    #     self.updated = itemDict['updated']
    #     self.priority = itemDict['priority']
    #     self.status = itemDict['status']
    #     self.created = itemDict['created']
    #     pass

    def __updateWorkItemDetail(self) -> bool:
        global DbConn
        global DetailFields
        global FieldMap
        global AtlassianKey
        global SqlTables

        knownFields = SqlTables['workitem_detail']

        # for key in knownFields:
        #     if key not in DetailFields.keys():
        #         insertList.append('')
        #         continue # table columns that do not match a field from issue are skipped
        #     value = DetailFields[key]
        #     if isinstance(value, str):
        #         insertList.append(value)
        #         continue # strings are expected so we move on
        #     insertList.append(value['displayName'])
        
        insertList = [None]
        # 'id'
        if 'atlassian_keyid' in DetailFields.keys(): insertList.append(DetailFields['atlassian_keyid'])
        if 'assignee' in DetailFields.keys(): insertList.append(DetailFields['assignee']['displayName'])
        if 'reporter' in DetailFields.keys(): insertList.append(DetailFields['reporter']['displayName'])
        if 'summary' in DetailFields.keys(): insertList.append(DetailFields['summary'])
        if 'updated' in DetailFields.keys(): insertList.append(DetailFields['updated'])
        if 'priority' in DetailFields.keys(): insertList.append(int(DetailFields['priority']['id']))

        if 'status' in DetailFields.keys(): insertList.append(DetailFields['status'])

        if 'created' in DetailFields.keys(): insertList.append(DetailFields['created'])

        if 'issue_type' in DetailFields.keys(): insertList.append(DetailFields['issue_type'])

        if 'request_type' in DetailFields.keys(): insertList.append(DetailFields['request_type'])

        sql = f'INSERT INTO workitem_detail({','.join(SqlTables['workitem_details'])}) VALUES(?,?,?,?,?,?,?,?,?,?,?)'

        cursor = DbConn.execute(sql, tuple(insertList))

        return True


    # update workitem_detail table
    def __updateWorkItemChangelog(self) -> bool:
        global DbConn
        global ChangeLogList
        global AtlassianKey

        

        return True
    

    def normalizeFieldsToSqlColumns(self, aDetailFields : dict, aFieldMap : dict):
        global DetailFields
        # TODO use DbConn.SqlTables or something to match the detail fields with the sql column names using
        # field map to verify they're right
        # mainly need to split the issue type, request type, and status


    def saveWorkItem(self,
            aDetailFields : dict,
            aFieldMap : dict,
            aChangelogList : list):
        global DetailFields
        global FieldMap
        global ChangeLogList
        global AtlassianKey

        DetailFields = aDetailFields
        FieldMap = aFieldMap
        ChangeLogList = aChangelogList
        AtlassianKey = DetailFields['atlassian_keyid']

        functions = [
            self.__updateWorkItemDetail,
            self.__updateWorkItemChangelog
        ]

        for func in functions:
            if not func(): raise SystemError(f"! Database update failed in {func}.")

        pass
