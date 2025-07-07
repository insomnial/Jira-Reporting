# Jira-Reporting
Python project using an separate API repository to search for Jira/JSM issues and generate reports on them.

## Populate requirements which you'll need to install
(in the venv) `pip freeze > requirements.txt`

## Add export and unset variables in  or  script

### `.venv/bin/activate`
```
export ATLASSIAN_EMAIL=""
export ATLASSIAN_KEY=""
export ATLASSIAN_ROOTURL=""
```
and
```
unset ATLASSIAN_EMAIL
unset ATLASSIAN_KEY
unset ATLASSIAN_ROOTURL
```

### `.venv\Scripts\Activate.ps1`
```
$env:ATLASSIAN_EMAIL = ''
$env:ATLASSIAN_KEY = ''
$env:ATLASSIAN_ROOTURL = ''
```
and
```
Remove-Item ENV:\ATLASSIAN_EMAIL
Remove-Item ENV:\ATLASSIAN_KEY
Remove-Item ENV:\ATLASSIAN_ROOTURL
```

## Logging in stdout
1. `* Local db`
   - Information steps
2. `> Check for db folder`
   - Action
3. `! Db folder does not exist`
   - Action results
4. `# Get issues from filter sql property`
   - Process step
 
