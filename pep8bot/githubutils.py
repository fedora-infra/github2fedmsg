import requests
import json
import logging
log = logging.getLogger("github")

from githubsecrets import secret_oauth_token

oauth_dict = dict(access_token=secret_oauth_token)
my_name = 'pep8bot'
prefix = "https://api.github.com"


def my_fork(username, repo):
    url = prefix + "/repos/%s/%s/forks" % (username, repo)
    response = requests.get(url, params=oauth_dict)
    for fork in response.json:
        if my_name is fork['owner']['login']:
            return fork

    # I must not have forked it yet..
    return None


def create_fork(username, repo):
    """
    http://developer.github.com/v3/repos/forks/#create-a-fork
    """
    log.info("Creating github fork of %s/%s" % (username, repo))
    url = prefix + "/repos/%s/%s/forks" % (username, repo)
    response = requests.post(url, params=oauth_dict)

    if not response.status_code == 202:
        raise IOError(response.status_code)

    log.debug("Successful.")

    return response.json


def default_branch(username, repo):
    log.info("Querying default branch of %s/%s" % (username, repo))
    url = prefix + "/repos/%s/%s" % (username, repo)
    response = requests.get(url, params=oauth_dict)

    if not response.status_code == 200:
        raise IOError(response.status_code)

    log.debug("Successful (%r)." % response.json['master_branch'])
    return response.json['master_branch']


pull_request_body = "Melissa is a babe!"


def create_pull_request(username, repo, patch_branch):
    """
    http://developer.github.com/v3/pulls/#create-a-pull-request
    """
    log.info("Creating github pull request on %s/%s" % (username, repo))
    url = prefix + "/repos/%s/%s/pulls" % (username, repo)
    branch = default_branch(username, repo)
    payload = dict(
        title='PEP8 Cleanup',
        body=pull_request_body,
        base=branch,
        head="pep8bot:" + patch_branch,
    )
    response = requests.post(url, params=oauth_dict, data=json.dumps(payload))

    if not response.status_code == 201:
        raise IOError(response.status_code)

    log.debug("Successful.")

    return response.json


def post_status(username, repo, sha, state):
    """
    http://developer.github.com/v3/repos/statuses/#create-a-status
    """
    description_lookup = {
        "success": "PEP8bot says \"OK\",
        "failure": "PEP8bot detected errors",
        "pending": "Still waiting on PEP8bot check",
        "error": "PEP8bot ran into trouble",
    }
    log.info("Posting status on %s/%s#%s" % (username, repo, sha))
    url = prefix + "/repos/%s/%s/statuses/%s" % (username, repo, sha)
    payload = dict(
        state=state,
        # TODO -- include target_url
        #target_url="...",
        description=description_lookup[state],
    )
    raise NotImplementedError("oauth-dict must have a user-specific token")
    response = requests.post(url, params=oauth_dict, data=json.dumps(payload))

    if not response.status_code == 201:
        raise IOError(response.status_code)

    log.debug("Successful.")

    return response.json
