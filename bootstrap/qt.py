import os
import subprocess
import json
import bootstrap.utils as utl
from pprint import pprint

_cd = os.path.dirname(os.path.abspath(__file__))


def qmlimportscanner(qt_path, rootQmlDir):
    qmlis = os.path.join(qt_path, 'bin', 'qmlimportscanner')

    if not os.path.exists(qmlis):
        raise Exception("qmlimportscanner was not found in {}".format(qmlis))

    cmd = [
        qmlis,
        '-rootPath',
        rootQmlDir,
        '-importPath',
        rootQmlDir,
        os.path.join(qt_path, 'qml')
    ]

    err, out = utl.run(cmd)

    if err:
        raise Exception("qmlimportscanner error: " + str(err))

    return json.loads(out)
