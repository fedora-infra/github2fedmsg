import json
import hmac
import hashlib
import urllib
import requests

payload = {
    "after": "3ef21292dd6448d4731f49864844d458ad3801a5",
    "before": "541d26405960ef934a398d7ee413bf7855cbe220",
    "commits": [
        { "added": [],
         "author": { "email": "rbean@redhat.com",
                    "name": "Ralph Bean",
                    "username": "ralphbean" },
         "committer": { "email": "rbean@redhat.com",
                       "name": "Ralph Bean",
                       "username": "ralphbean" },
         "distinct": True,
         "id": "81eacd09c4d6526bea1d14e3fbc17ef0fd1d9192",
         "message": "Authentication policy.",
         "modified": [ "statatat/__init__.py",
                      "statatat/views.py" ],
         "removed": [],
         "timestamp": "2012-08-25T06:30:21-07:00",
         "url": "https://github.com/ralphbean/statatat/commit/81eacd09c4d6526bea1d14e3fbc17ef0fd1d9192" },
        { "added": [],
         "author": { "email": "rbean@redhat.com",
                    "name": "Ralph Bean",
                    "username": "ralphbean" },
         "committer": { "email": "rbean@redhat.com",
                       "name": "Ralph Bean",
                       "username": "ralphbean" },
         "distinct": True,
         "id": "ffedad58abec3cbf6546daedfb4249db5b994203",
         "message": "Use BeforeRender like a pro.",
         "modified": [ "statatat/views.py" ],
         "removed": [],
         "timestamp": "2012-08-25T06:36:24-07:00",
         "url": "https://github.com/ralphbean/statatat/commit/ffedad58abec3cbf6546daedfb4249db5b994203" },
        { "added": [],
         "author": { "email": "rbean@redhat.com",
                    "name": "Ralph Bean",
                    "username": "ralphbean" },
         "committer": { "email": "rbean@redhat.com",
                       "name": "Ralph Bean",
                       "username": "ralphbean" },
         "distinct": True,
         "id": "3ef21292dd6448d4731f49864844d458ad3801a5",
         "message": "Keep \"identity\" in the globals like TG2.",
         "modified": [ "statatat/views.py" ],
         "removed": [],
         "timestamp": "2012-08-25T06:37:21-07:00",
         "url": "https://github.com/ralphbean/statatat/commit/3ef21292dd6448d4731f49864844d458ad3801a5"
        }
    ],
    "compare": "https://github.com/ralphbean/statatat/compare/541d26405960...3ef21292dd64",
    "created": False,
"deleted": False,
"forced": False,
"head_commit": { "added": [],
                "author": { "email": "rbean@redhat.com",
                           "name": "Ralph Bean",
                           "username": "ralphbean" },
                "committer": { "email": "rbean@redhat.com",
                              "name": "Ralph Bean",
                              "username": "ralphbean" },
                "distinct": True,
                "id": "3ef21292dd6448d4731f49864844d458ad3801a5",
                "message": "Keep \"identity\" in the globals like TG2.",
                "modified": [ "statatat/views.py" ],
                "removed": [],
                "timestamp": "2012-08-25T06:37:21-07:00",
                "url": "https://github.com/ralphbean/statatat/commit/3ef21292dd6448d4731f49864844d458ad3801a5" },
"pusher": { "name": "none" },
"ref": "refs/heads/master",
"repository": { "created_at": "2012-07-05T21:22:12-07:00",
               "description": "Embeddable realtime dev widgets.",
               "fork": False,
               "forks": 0,
               "has_downloads": True,
               "has_issues": True,
               "has_wiki": False,
               "language": "Python",
               "master_branch": "develop",
               "name": "statatat",
               "open_issues": 3,
               "owner": { "email": "ralph.bean@gmail.com",
                         "name": "ralphbean" },
               "private": False,
               "pushed_at": "2012-09-16T20:03:33-07:00",
               "size": 272,
               "stargazers": 3,
               "url": "https://github.com/ralphbean/statatat",
               "watchers": 3 } }

blob = {'payload': json.dumps(payload)}

github_secret = 'changeme!'
body = urllib.urlencode(blob)
hex = hmac.new(github_secret, body, hashlib.sha1).hexdigest()
headers = {
    'X-Hub-Signature': 'sha1=%s' % hex,
}

response = requests.post(
    "http://localhost:6543/webhook",
    data=blob,
    headers=headers,
)

print response.status_code
print response.text
