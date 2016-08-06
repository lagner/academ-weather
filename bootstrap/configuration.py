import os
import logging as log
import configparser

_cd = os.path.dirname(os.path.abspath(__file__))


def init_config(args):
    conf = __read_default()
    select_ndk(conf, args)

    conf.set('android', 'arch', args.arch)

    if not args.qt:
        key = 'qt.{}.dir'.format(args.arch)
        qt = conf.get('local', key, fallback='')
        conf.set('default', 'qt', qt)

    return conf


def __read_default():
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )

    config_path = os.path.join(_cd, '..', 'config.cfg')
    if os.path.exists(config_path):
        parser.read(config_path)
    else:
        log.debug("global config is not exist")

    local_props = os.path.join(_cd, '..', 'android', 'local.properties')
    if os.path.exists(local_props):
        props = __parse_properties(local_props)
        parser.read_dict({'local': props})
    return parser


def __parse_properties(filename='local.properties'):
    keys = dict()
    with open(filename, 'r') as properties:
        for line in properties:
            line = line.strip()

            if line.startswith('#'):
                continue

            # TODO: make it simpler
            parts = [s.strip() for s in line.split('=')]
            key = None
            value = None
            if parts:
                key = parts.pop(0)
            if parts:
                value = parts.pop(0)
            if key:
                keys[key] = value
    return keys


def select_ndk(conf, args):
    ndk = ""
    if args.ndk:
        ndk = os.path.abspath(args.ndk)
    else:
        ndk = conf.get('local', 'ndk.dir', fallback="")
    conf.set('DEFAULT', 'ndk', ndk)
