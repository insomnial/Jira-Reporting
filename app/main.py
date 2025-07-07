import sys, os, base64
from datetime import datetime
from atlassian_api_py import controllerapi
import controllerdb
import controllerwebhook
import controllerworkitems
from workitem import WorkItem


# constant strings
USAGE = "Start GUI by calling main.py\n" \
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


# Gets the work items associated with the specified filter
def _getWorkItemsUsingFilter(aFilter : str) -> None:
    global ApiCon
    global Keys

    print("# Get work items from filter's sql property")
    getFilter = ApiCon.get_filter(aFilter)
    filterSql = getFilter['jql']
    isLast = False
    nextPageToken = ''
    Keys = []
    while not isLast:
        search = ApiCon.search_jql(aJql=filterSql, nextPageToken=nextPageToken, maxResults=1000)
        if 'isLast' in search: isLast = search['isLast']
        if 'nextPageToken' in search: nextPageToken = search['nextPageToken']
        issues = search['issues']
        for item in issues:
            key = item['key']
            Keys.append(key)
        print(len(Keys))


# Gets work item details from list of key IDs
def _getWorkItemDetailsForKeys() -> None:
    global ApiCon
    global Keys

    print("Search for specific work items")
    for key in Keys:
        print(f"# {key}")
        print(f"  - Get issue details")
        # get issue details
        issueDetailsJson = ApiCon.get_issue(issueIdOrKey=key, fieldsByKeys=True)

        # filter out empty custom_field
        popFields = {k:v for k,v in issueDetailsJson['fields'].items() if v}
        popFields['atlassian_keyid'] = key

        pass

        # TODO Get issues details: assignee, status, created date, updated date

        # get issue changelogs
        print(f"  - Get issue changelogs")
        isLast = False
        startAt = 0
        changelogs = []
        while not isLast:
            changelogJson = ApiCon.get_changelogs(key)
            isLast = changelogJson['isLast']
            startAt = startAt + changelogJson['total']
            changelogs = changelogs + changelogJson['values']
            pass # while

        print(f"  - Store work item in {DbCon}")
        workItem = WorkItem(DbCon).saveWorkItem(popFields, issueDetailsJson['names'], changelogs)

        # TODO Parse changelogs and track: assignee changes, status changes

        pass # for


def main(cmds = None, args = None, opts = None) -> None:
    global ApiCon
    global DbCon

    if not args:
        raise SystemExit(USAGE)
    
    if CMD_NOGUI in cmds:
        print(f"* Running in terminal")
    else:
        print(f"* Starting gui")
        print(f"NOT CURRENTLY SUPPORTED")
        raise SystemExit(0)

    if '-filter' not in opts:
        raise SystemExit(USAGE)

    reqFilter = args[opts.index('-filter')]

    # get atlassian env
    email = os.getenv('ATLASSIAN_EMAIL')
    key = os.getenv('ATLASSIAN_KEY')
    # workspaceid = os.getenv('ATLASSIAN_WORKSPACEID')
    rooturl = os.getenv('ATLASSIAN_ROOTURL')
    token = base64.b64encode(f'{email}:{key}'.encode()).decode()
    
    # get API controller
    ApiCon = controllerapi.ApiController(aToken=token, aRootUrl=rooturl)

    # get DB
    now = datetime.now() # current date and time
    date_time = now.strftime("%m%d%Y%H%M%S")
    if CMD_VOLATILE in cmds:
        print(f"* Memory db")
        DbCon = controllerdb.init()
    else:
        print(f"* Local db")
        DbCon = controllerdb.init(date_time + '.db')

    # get list of work items from filter
    keys = _getWorkItemsUsingFilter(aFilter=reqFilter)
    print()

    # details from each work item
    _getWorkItemDetailsForKeys()

    pass # main


if __name__ == "__main__":
    cmds = [cmd for cmd in sys.argv[1:] if cmd.startswith("--")]
    opts = [opt for opt in sys.argv[1:] if (opt.startswith("-") and not opt.startswith("--"))]
    args = [arg for arg in sys.argv[1:] if (not arg.startswith("-") and not arg.startswith("--"))]

    try:
        main(cmds, args, opts)
    except KeyboardInterrupt as e:
        print(f"\n\n####\nClosing script.")
