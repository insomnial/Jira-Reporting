import sys
import os
import base64
from datetime import datetime

from atlassian_api_py import controllerapi

import controllerdb
import controllerwebhook
from workitems.WorkItemController import WorkItemController
from reports.TotalPerMonthReport import TotalPerMonthReport
from reports.TimeToFirstResponseAverageReport import TimeToFirstResponseAverageReport
from reports.TimeToResolutionAverageReport import TimeToResolutionAverageReport

# constant strings
USAGE = "Start by calling main.py OPT REQ\n" \
        "  OPT\n" \
        "    [--volatile] for memory db, defaults to local db\n" \
        "    [--nogui] to run in terminal\n" \
        "  REQ\n" \
        "    [-filter <filter_id>] must be readable by user credentials\n"

# constant args
CMD_VOLATILE = '--volatile'
CMD_NOGUI = '--nogui'

# globals
ApiCon = None
DbCon = None
Keys = None
Version = '20250713e'


def main(cmds = None, args = None, opts = None) -> None:
    global ApiCon
    global DbCon
    global Version

    if not args:
        raise SystemExit(USAGE)
    
    # treat all instances as no gui for the moment
    # if CMD_NOGUI in cmds:
    #     print(f"* Starting terminal")
    # else:
    #     print(f"* Starting gui")
    #     print(f"NOT CURRENTLY SUPPORTED")
    #     raise SystemExit(0)

    if '-filter' not in opts:
        raise SystemExit(USAGE)

    requestFilter = args[opts.index('-filter')]

    # get atlassian env
    email = os.getenv('ATLASSIAN_EMAIL')
    key = os.getenv('ATLASSIAN_KEY')
    # workspaceid = os.getenv('ATLASSIAN_WORKSPACEID')
    rooturl = os.getenv('ATLASSIAN_ROOTURL')
    token = base64.b64encode(f'{email}:{key}'.encode()).decode()
    
    # instantiate API controller
    ApiCon = controllerapi.ApiController(aToken=token, aRootUrl=rooturl)

    # instantiate WorkItemController
    WorkItemCon = WorkItemController(ApiCon)

    # get DB
    now = datetime.now() # current date and time
    date_time = now.strftime("%m%d%Y%H%M%S")
    dbfilename = f'jira_reporting_{Version}.db'
    if CMD_VOLATILE in cmds:
        print(f"* Memory db")
        DbCon = controllerdb.init()
    else:
        print(f"* Local db")
        # DbCon = controllerdb.init(date_time + '.db')
        DbCon = controllerdb.init(dbfilename)

    WorkItemCon.setDatabaseConnection(DbCon)

    # start populating work items from filter
    WorkItemCon.loadFromFilter(requestFilter)

    # start report generation
    reports = [
        TotalPerMonthReport(FilterName=WorkItemCon.FilterName, WorkItemList=WorkItemCon.getWorkItems()),
        TimeToFirstResponseAverageReport(FilterName=WorkItemCon.FilterName, WorkItemList=WorkItemCon.getWorkItems()),
        TimeToResolutionAverageReport(FilterName=WorkItemCon.FilterName, WorkItemList=WorkItemCon.getWorkItems())
    ]
    for report in reports:
        report.generate().save()


if __name__ == "__main__":
    cmds = [cmd for cmd in sys.argv[1:] if cmd.startswith("--")]
    opts = [opt for opt in sys.argv[1:] if (opt.startswith("-") and not opt.startswith("--"))]
    args = [arg for arg in sys.argv[1:] if (not arg.startswith("-") and not arg.startswith("--"))]

    try:
        main(cmds, args, opts)
    except KeyboardInterrupt as e:
        print(f"\n\n####\nClosing script.")
        if DbCon:
            DbCon.close()
        sys.exit(0)
