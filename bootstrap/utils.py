import os
import subprocess
import logging as log
from shutil import copy2
from contextlib import contextmanager


@contextmanager
def pushd(newDir):
    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
            return func
    return decorate


def run(cmd, check_code=False):
    shell = isinstance(cmd, str)
    try:
        log.debug('run: ' + (cmd if shell else ' '.join(cmd)))
        output = subprocess.check_output(
            cmd,
            shell=shell,
            universal_newlines=True
        )
        return 0, output
    except subprocess.CalledProcessError as ex:
        log.debug("called proces exception: " + str(ex))
        if check_code:
            raise
        else:
            return ex.returncode, ex.output


def sync_file(source, target):
    if os.path.exists(target):
        s = os.path.getmtime(source)
        t = os.path.getmtime(target)
        if t >= s:
            return

    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    copy2(source, target)


def sync_dir(source, target, remove_extra=False):
    join = os.path.join

    root, dirs, files = next(os.walk(source))

    for d in dirs:
        sync_dir(join(source, d), join(target, d), remove_extra=remove_extra)

    for f in files:
        sync_file(join(source, f), join(target, f))

    if remove_extra:
        *_, tfiles = next(os.walk(target))
        for extra in (set(tfiles) - set(files)):
            os.remove(extra)
        # FIXME: remove extra dirs


def fs_walk(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            yield os.path.join(root, filename)


def filenames_filter(files, extensions):
    for filename in files:
        basename, ext = os.path.splitext(filename)
        if ext in extensions:
            yield filename
