# Jira-Reporting
Python project using an separate API repository to search for Jira/JSM issues and generate reports on them.

## Populate requirements which you'll need to install
(in the venv) `pip freeze > requirements.txt`

## Add export and unset variables in activate script
Highly recommended to use venv.

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
 
## Example output
```
{
  "Name": "Average Time to First Reponse for previous 12 months",
  "FilterName": "ITDESK Incidents (All)",
  "KeyLabel": "IT Time to First Response",
  "Data": {
    "July 2025": "2m 20s",
    "June 2025": "19m 21s",
    "May 2025": "1m 55s",
    "April 2025": "1m 43s",
    "March 2025": "7m 49s",
    "February 2025": "5m 11s",
    "January 2025": "1m 8s",
    "December 2024": null,
    "November 2024": null,
    "October 2024": null,
    "September 2024": null
  }
}
```

```
{
  "Name": "Average Time to Resolution for previous 12 months",
  "FilterName": "ITDESK Incidents (All)",
  "KeyLabel": "IT Time to Resolution",
  "Data": {
    "July 2025": "523m 44s",
    "June 2025": "50m 41s",
    "May 2025": "34m 40s",
    "April 2025": "17m 45s",
    "March 2025": "37m 3s",
    "February 2025": "11m 27s",
    "January 2025": "5m 59s",
    "December 2024": null,
    "November 2024": null,
    "October 2024": null,
    "September 2024": null
  }
}
```

```
{
  "Name": "Total per month for previous 12 months",
  "FilterName": "ITDESK Incidents (All)",
  "Data": {
    "July 2025": 4,
    "June 2025": 19,
    "May 2025": 10,
    "April 2025": 19,
    "March 2025": 5,
    "February 2025": 7,
    "January 2025": 19,
    "December 2024": 7,
    "November 2024": 4,
    "October 2024": 14,
    "September 2024": 9
  }
}
```
