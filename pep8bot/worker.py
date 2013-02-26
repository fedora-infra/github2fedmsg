#!/usr/bin/env python

# stdlib
import tempfile
import time
import os
import shutil
import sys
import uuid

# pypi
import sh
from retask.queue import Queue
from sqlalchemy import engine_from_config
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

import pep8

# local
import pep8bot.githubutils as gh
import pep8bot.models as m


class directory(object):
    """ pushd/popd context manager. """
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self, *args, **kw):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, *args, **kw):
        os.chdir(self.savedPath)


class Worker(object):
    """ Represents the worker process.  Waits for tasks to come in from the
    webapp and then acts on them.
    """

    def __init__(self, config_uri):
        setup_logging(config_uri)
        settings = get_appsettings(config_uri, name="pep8bot")
        engine = engine_from_config(settings, 'sqlalchemy.')
        m.DBSession.configure(bind=engine)

        # TODO -- pass in redis params from config, hostname, etc.
        self.queue = Queue('commits')
        self.queue.connect()
        # TODO -- set both of these with the config file.
        # Use pyramid tools to load config.
        self.sleep_interval = 1
        self.scratch_dir = "/home/threebean/scratch/pep8bot-scratch"
        try:
            os.makedirs(self.scratch_dir)
        except OSError:
            pass  # Assume that the scratch_dir already exists.

    def run(self):
        while True:
            time.sleep(self.sleep_interval)
            task = self.queue.wait()
            data = task.data

            repo = data['reponame']
            owner = data['username']
            commits = data['commits']
            _user = m.User.query.filter_by(username=owner).one()

            token = _user.oauth_access_token
            if not token:
                for u in _user.users:
                    if u.oauth_access_token:
                        token = u.oauth_access_token

            clone_url = data['clone_url']

            self.working_dir = tempfile.mkdtemp(
                prefix=owner + '-' + repo,
                dir=self.scratch_dir,
            )

            print "** Cloning to", self.working_dir
            print sh.git.clone(clone_url, self.working_dir)

            lookup = {
                "success": "PEP8bot says \"OK\"",
                "failure": "PEP8bot detected {n} errors",
                "pending": "Still waiting on PEP8bot check",
                "error": "PEP8bot ran into trouble",
            }
            print "** Processing commits."
            for sha in commits:
                # TODO -- what about hash collisions?
                _commit = m.Commit.query.filter_by(sha=sha).first()
                import transaction
                try:
                    print "** Processing files on commit", sha
                    with directory(self.working_dir):
                        print sh.git.checkout(sha)

                    # TODO -- only process those in modified and added
                    infiles = []
                    for root, dirs, files in os.walk(self.working_dir):

                        if '.git' in root:
                            continue

                        infiles.extend([
                            root + "/" + fname
                            for fname in files
                            if fname.endswith(".py")
                        ])

                    # TODO -- document that the user can keep a .config/pep8
                    # file in their project dir.
                    pep8style = pep8.StyleGuide(
                        quiet=True,
                        config_file="./.config/pep8",
                    )
                    result = pep8style.check_files(infiles)

                    if result.total_errors > 0:
                        status = "failure"
                    else:
                        status = "success"

                    desc = lookup[status].format(n=result.total_errors)
                    _commit.status = status
                    gh.post_status(owner, repo, sha, status, token, desc)
                except Exception:
                    status = "error"
                    desc = lookup[status]
                    _commit.status = status
                    gh.post_status(owner, repo, sha, status, token, desc)
                    raise
                finally:
                    transaction.commit()


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def worker(config_filename):
    w = Worker(config_filename)
    try:
        w.run()
    except KeyboardInterrupt:
        pass


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    worker(sys.argv[1])

if __name__ == '__main__':
    main()
