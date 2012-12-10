import requests
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

    import pprint
    pprint.pprint(response.json)

    return response.json
