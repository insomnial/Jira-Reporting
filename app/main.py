import sys, os, base64
from datetime import datetime
from atlassian_api_py import controllerapi
import controllerdb
import controllerworkitems


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


# Gets the work items associated with the specified filter
# aConnApi : controllerapi object
# aFilter : filter ID from CLI
# return : populated list of key IDs
def _getWorkItemsUsingFilter(aConnApi : controllerapi, aFilter : str) -> list:
    print("# Get work items from filter's sql property")
    getFilter = aConnApi.get_filter(aFilter)
    filterSql = getFilter['jql']
    isLast = False
    nextPageToken = ''
    keys = []
    while not isLast:
        search = aConnApi.search_jql(aJql=filterSql, nextPageToken=nextPageToken)
        if 'isLast' in search: isLast = search['isLast']
        if 'nextPageToken' in search: nextPageToken = search['nextPageToken']
        issues = search['issues']
        for item in issues:
            key = item['key']
            keys.append(key)
        print(len(keys))
    return keys


# Gets work item details from list of key IDs
# aConnApi : controllerapi object
# aKeys : list of key IDs
def _getWorkItemDetails(aConnApi : controllerapi, aKeys : list) -> None:
    print("Search for specific work items")
    for key in aKeys:
        print(f"# {key}")
        print(f"  - Get issue details")
        # get issue details
        issueDetailsJson = aConnApi.get_issue(issueIdOrKey=key, fieldsByKeys=True)
        print(f"  - Save issue details")
        # TODO Get issues details: assignee, status, created date, updated date

        # get issue changelogs
        print(f"  - Get issue changelogs")
        isLast = False
        startAt = 0
        changelogs = []
        while not isLast:
            changelogJson = aConnApi.get_changelogs(key)
            isLast = changelogJson['isLast']
            startAt = startAt + changelogJson['total']
            changelogs = changelogs + changelogJson['values']
            pass # while
        print(f"  - Save changelogs")
        # TODO Parse changelogs and track: assignee changes, status changes

        pass # for


def main(cmds = None, args = None, opts = None) -> None:
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
    conapi = controllerapi.ApiController(aToken=token, aRootUrl=rooturl)

    # get DB
    now = datetime.now() # current date and time
    date_time = now.strftime("%m%d%Y%H%M%S")
    if CMD_VOLATILE in cmds:
        print(f"* Memory db")
        dataDb = controllerdb.init()
    else:
        print(f"* Local db")
        dataDb = controllerdb.init(date_time + '.db')

    # get list of work items from filter
    keys = _getWorkItemsUsingFilter(aConnApi=conapi, aFilter=reqFilter)
    print()

    # details from each work item
    _getWorkItemDetails(aConnApi=conapi, aKeys=keys)
    
    pass # main


if __name__ == "__main__":
    cmds = [cmd for cmd in sys.argv[1:] if cmd.startswith("--")]
    opts = [opt for opt in sys.argv[1:] if (opt.startswith("-") and not opt.startswith("--"))]
    args = [arg for arg in sys.argv[1:] if (not arg.startswith("-") and not arg.startswith("--"))]

    try:
        main(cmds, args, opts)
    except KeyboardInterrupt as e:
        print(f"\n\n####\nClosing script.")
