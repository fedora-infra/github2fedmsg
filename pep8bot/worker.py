
# stdlib
import tempfile
import time
import pprint
import os
import shutil
import uuid

# pypi
import sh
from retask.queue import Queue

import pep8

# local
import githubutils as gh


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

    def __init__(self):
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
            print "Waking"
            if self.queue.length == 0:
                continue

            task = self.queue.dequeue()
            data = task.data

            repo = data['repository']['name']
            owner = data['repository']['owner']['name']
            commits = data['commits']
            import pprint
            pprint.pprint(commits)

            fork = gh.my_fork(owner, repo)
            if not fork:
                fork = gh.create_fork(owner, repo)
                print "Sleeping for 4 seconds"
                time.sleep(4)

            url = fork['ssh_url']

            self.working_dir = tempfile.mkdtemp(
                prefix=owner + '-' + repo,
                dir=self.scratch_dir,
            )

            print "** Cloning to", self.working_dir
            print sh.git.clone(url, self.working_dir)

            print "** Adding remote upstream"
            with directory(self.working_dir):
                print sh.git.remote.add("upstream", data['repository']['url'])
                print sh.git.pull("upstream",
                                  data['repository']['master_branch'])

            print "** Processing commits."
            for commit in commits:
                print "** Processing files on commit", commit
                print sh.git.checkout(commit)
                infiles = []
                for root, dirs, files in os.walk(self.working_dir):

                    if '.git' in root:
                        continue

                    infiles.extend([
                        root + "/" + fname
                        for fname in files
                        if fname.endswith(".py")
                    ])

                pep8style = pep8.StyleGuide(quiet=True)
                result = pep8style.check_files(infiles)
                print result.total_errors
                # TODO - mark gh commit with errors
                # TODO - add a note in our DB about the status
                # TODO - try/except/finally mark as 'failed' if necessary.


def worker():
    w = Worker()
    try:
        w.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    worker()
