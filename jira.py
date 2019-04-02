import requests
import json
import os
import fire


class Status(object):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"


def ask_jira(host, jqlQuery):
    url = "{}/rest/api/3/search".format(host)
    token = os.environ.get("JIRA_TOKEN")

    headers = {
        "Authorization": "Basic " + token,
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "expand": [
            "names",
            "schema"
        ],
        "jql": jqlQuery,
        "maxResults": 30,
        "fieldsByKeys": False,
        "fields": [
            "summary",
            "status",
            "assignee",
            "name",
            "id",
            "key"
        ],
        "startAt": 0
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )
    return response


def get_resolved_issues(host, assignee, after, before):
    jqlQuery = ('project = AP AND assignee = "{0}"'
                ' AND resolved >= "{1}" AND resolved < "{2}"'
                ' AND sprint in openSprints()').format(assignee, after, before)
    response = ask_jira(host, jqlQuery)
    return json.dumps(json.loads(response.text),
                      sort_keys=True,
                      indent=4,
                      separators=(",", ": "))


def get_issues(host, assignee, status):
    jqlQuery = ('project = AP AND assignee = "{}"'
                ' AND status in ("{}")'
                ' AND sprint in openSprints()').format(assignee, status)

    response = ask_jira(host, jqlQuery)

    return json.dumps(json.loads(response.text),
                      sort_keys=True,
                      indent=4,
                      separators=(",", ": "))


if __name__ == "__main__":
    fire.Fire({
        'issues': get_issues,
        'resolved_issues': get_resolved_issues
    })
