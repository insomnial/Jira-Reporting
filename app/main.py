import sys, os, base64
from atlassian_api_py import controllerapi

USAGE = "Start GUI by calling main.py"

def main(args = None, opts = None) -> None:
    # if not args:
    #     raise SystemExit(USAGE)

    # if args[0] == "--help":
    #     raise SystemExit(USAGE)
    
    # get atlassian env
    email = os.getenv('ATLASSIAN_EMAIL')
    key = os.getenv('ATLASSIAN_KEY')
    workspaceid = os.getenv('ATLASSIAN_WORKSPACEID')
    rooturl = os.getenv('ATLASSIAN_ROOTURL')
    token = base64.b64encode(f'{email}:{key}'.encode()).decode()
    
    controller = controllerapi.ApiController(aToken=token, aRootUrl=rooturl, aWorkspace=workspaceid)

    print("Search using filter sql property")
    getFilter = controller.get_filter(10209)
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

    print("Seach for specific issues")
    for key in keys:
        # get issue details
        issueDetailsJson = controller.get_issue(issueIdOrKey=key, fieldsByKeys=True)
        # get issue changelogs
        isLast = False
        startAt = 0
        changelogs = []
        while not isLast:
            changelogJson = controller.get_changelogs(key)
            isLast = changelogJson['isLast']
            startAt = startAt + changelogJson['total']
            changelogs = changelogs + changelogJson['values']
            pass # while

        # TODO Get issues details: assignee, status, created date, updated date
        # TODO Parse changelogs and track: assignee changes, status changes

        pass # for
    
    pass # main


if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    main(args, opts)
