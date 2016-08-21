import os
import re
import subprocess
import json
import bootstrap.utils as utl
import logging as log
from xml.etree import ElementTree

_cd = os.path.dirname(os.path.abspath(__file__))

ARCH = ('armeabi-v7a', 'x86', 'mips')
ANDROID_PLUGIN = 'plugins/platforms/android/libqtforandroid.so'


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


@utl.static_vars(pattern=None)
def read_elf_dependencies(library, readelf="readelf"):
    cmd = (readelf, '-d', '-W', library)

    output = subprocess.check_output(cmd, universal_newlines=True)

    #  0x00000001 (NEEDED)   Shared library: [libQt5Network.so]
    if not read_elf_dependencies.pattern:
        read_elf_dependencies.pattern = re.compile(
            "^.*\(NEEDED\)\s+(Shared library:)\s+\[(?P<library>lib.*\.so)]\s*$")
    libs = set()

    for line in output.split('\n'):
        m = read_elf_dependencies.pattern.search(line)
        if m:
            library = m.groupdict().get('library', None)
            if library:
                libs.add(library)
    return libs


def qt_elf_dependencies(filepath, config):
    ndk_path = config.get('android', 'ndk')
    ndk_host = config.get('android', 'ndk-host')
    tch_prefix = config.get('android', 'toolchain-prefix')
    tch_version = config.get('android', 'toolchain-version')
    tool_prefix = config.get('android', 'tool_prefix')

    readelf = os.path.join(
        ndk_path,
        'toolchains',
        '{}-{}'.format(tch_prefix, tch_version),
        'prebuilt',
        ndk_host,
        'bin',
        '{}-readelf'.format(tool_prefix),
    )

    libs = read_elf_dependencies(filepath, readelf=readelf)

    qt_dir = config.get('default', 'qt')

    qt_libs = os.path.join(qt_dir, 'lib')
    extra_libs = set()
    for lib in libs:
        fullpath = os.path.join(qt_libs, lib)
        if not os.path.exists(fullpath):
            extra_libs.add(lib)
    return libs - extra_libs


def get_all_deps(lib, config):
    dependencies = set()
    libs_to_check = qt_elf_dependencies(lib, config)

    qt_libs = config.get('default', 'qt')
    qt_libs = os.path.join(qt_libs, 'lib')

    while libs_to_check:
        lib = libs_to_check.pop()
        dependencies.add(lib)

        fullpath = os.path.join(qt_libs, lib)
        deps = qt_elf_dependencies(fullpath, config)

        # libs in dependencies already checked
        extra = deps - dependencies
        libs_to_check.update(extra)

    return dependencies


def read_dependency_xml(moduleName, config):
    qt_path = config.get('default', 'qt')
    xml_path = os.path.join(
        qt_path, 'lib/{}-android-dependencies.xml'.format(moduleName))
    if not os.path.exists(xml_path):
        log.info("module {} do not have xml {}".format(moduleName, xml_path))
        return

    tree = ElementTree.parse(xml_path)
    root = tree.getroot()
    lib_tag = root.find('dependencies/lib')

    name = "" if not lib_tag.attrib else lib_tag.attrib.get('name', "")

    if name != moduleName:
        raise Exception("moduleName({}) and name from xml({}) do not match".format(
            moduleName, name))

    deps_tag = lib_tag.find('depends')
    deps = list()

    for child in deps_tag:
        info = {
            "tag": child.tag
        }
        info.update(child.attrib)
        deps.append(info)

    return deps
