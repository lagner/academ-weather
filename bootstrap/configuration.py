import os
import logging as log
import configparser

_cd = os.path.dirname(os.path.abspath(__file__))


def initConfig():
    parser = configparser.ConfigParser()

    config_path = os.path.join(_cd, '..', 'config.cfg')
    if os.path.exists(config_path):
        parser.read(config_path)
    else:
        log.debug("global config is not exist")

    local_props = os.path.join(_cd, '..', 'android', 'local.properties')
    if os.path.exists(local_props):
        props = parse_properties(local_props)
        parser.read_dict({'local': props})
    return parser


def parse_properties(filename='local.properties'):
    keys = dict()
    with open(filename, 'r') as properties:
        line = properties.readline()
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


config = initConfig()

__all__ = ['config', ]
