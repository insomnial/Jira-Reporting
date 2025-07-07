import sys, os, base64
from atlassian_api_py import controllerapi
import controllerdb
from datetime import datetime

# constant strings
USAGE = "Start GUI by calling main.py\n" \
        "  OPT\n" \
        "    --volatile for memory db, defaults to local db\n" \
        "  REQ\n" \
        "    -filter <filter_id>\n"

# constant args
CMD_VOLATILE = '--volatile'


def main(cmds = None, args = None, opts = None) -> None:
    if not args:
        raise SystemExit(USAGE)

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
    controller = controllerapi.ApiController(aToken=token, aRootUrl=rooturl, aWorkspace=workspaceid)

    # get DB
    now = datetime.now() # current date and time
    date_time = now.strftime("%m%d%Y%H%M%S")
    if CMD_VOLATILE in cmds:
        print(f"* Memory db")
        dataDb = controllerdb.init()
    else:
        print(f"* Local db")
        dataDb = controllerdb.init(date_time + '.db')

    # move this to its own method?
    print("# Get issues from filter sql property")
    getFilter = controller.get_filter(reqFilter)
    filterSql = getFilter['jql']
    isLast = False
    nextPageToken = ''
    keys = []
    while not isLast:
        search = controller.search_jql(aJql=filterSql, nextPageToken=nextPageToken)
        if 'isLast' in search: isLast = search['isLast']
        if 'nextPageToken' in search: nextPageToken = search['nextPageToken']
        issues = search['issues']
        for item in issues:
            key = item['key']
            keys.append(key)
        print(len(keys))
        pass
    print()

    print("Search for specific issues")
    for key in keys:
        print(f"# {key}")
        print(f"  - Get issue details")
        # get issue details
        issueDetailsJson = controller.get_issue(issueIdOrKey=key, fieldsByKeys=True)
        print(f"  - Save issue details")
        # TODO Get issues details: assignee, status, created date, updated date

        # get issue changelogs
        print(f"  - Get issue changelogs")
        isLast = False
        startAt = 0
        changelogs = []
        while not isLast:
            changelogJson = controller.get_changelogs(key)
            isLast = changelogJson['isLast']
            startAt = startAt + changelogJson['total']
            changelogs = changelogs + changelogJson['values']
            pass # while
        print(f"  - Save changelogs")
        # TODO Parse changelogs and track: assignee changes, status changes

        pass # for
    
    pass # main


if __name__ == "__main__":
    cmds = [cmd for cmd in sys.argv[1:] if cmd.startswith("--")]
    opts = [opt for opt in sys.argv[1:] if (opt.startswith("-") and not opt.startswith("--"))]
    args = [arg for arg in sys.argv[1:] if (not arg.startswith("-") and not arg.startswith("--"))]

    main(cmds, args, opts)
