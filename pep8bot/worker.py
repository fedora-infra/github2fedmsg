
# stdlib
import tempfile
import time
import pprint
import os
import shutil

# pypi
import sh
from retask.task import Task
from retask.queue import Queue

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

            fork = gh.my_fork(owner, repo)
            if not fork:
                fork = gh.create_fork(owner, repo)

            url = fork['url']

            self.working_dir = tempfile.mkdtemp(
                prefix=owner + '-' + name,
                dir=self.scratch_dir,
            )

            # TODO -- what if our fork is out of date of their upstream?  We
            # need to "git pull --force # or something"
            print "** Cloning to", self.working_dir
            print sh.git.clone(url, self.working_dir)
            print "** Processing files."
            for root, dirs, files in os.walk(self.working_dir):

                if '.git' in root:
                    continue

                for filename in files:
                    if filename.endswith(".py"):
                        infile = root + "/" + filename
                        print "** Tidying", infile
                        tmpfile = infile + ".bak"
                        script = os.path.expanduser(
                            "~/devel/PythonTidy/PythonTidy.py"
                        )
                        sh.python(script, infile, tmpfile)
                        shutil.move(tmpfile, infile)

            with directory(self.working_dir):
                print sh.pwd()
                print sh.git.status()

            # TODO
            # 1) commit
            # 2) push
            # 3) create pull request


def worker():
    w = Worker()
    try:
        w.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    worker()
