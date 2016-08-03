import os
import re
import subprocess
import json
import bootstrap.utils as utl

_cd = os.path.dirname(os.path.abspath(__file__))

ARCH = ('armeabi-v7a', 'x86', 'mips')


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


def read_elf_dependensies(args, filepath):
    readelf = os.path.join(
        args.ndk,
        'toolchains',
        '{}-{}'.format(args.toolchain_prefix, args.toolchain_version),
        'prebuilt',
        args.ndk_host,
        'bin',
        '{}-readelf'.format(args.tool_prefix),
    )
    cmd = (readelf, '-d', '-W', filepath)

    output = subprocess.check_output(cmd, universal_newlines=True)

    #  0x00000001 (NEEDED)   Shared library: [libQt5Network.so]
    regexp = re.compile("^.*\(NEEDED\)\s+(Shared library:)\s+\[(?P<library>lib.*\.so)]\s*$")
    libs = set()

    for line in output.split('\n'):
        m = regexp.search(line)
        if m:
            library = m.groupdict().get('library', None)
            if library:
                libs.add(library)
    return libs
