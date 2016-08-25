import os
import logging as log
from xml.etree import ElementTree


class AndroidManifest:
    XMLNS = {
        'android': 'http://schemas.android.com/apk/res/android'
    }
    ElementTree.register_namespace('android', XMLNS['android'])

    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("manifest is not exist here: {}".format(path))
        self.tree = ElementTree.parse(path)
        self.root = self.tree.getroot()

    def has_feature(self, feature):
        query = './uses-feature[@android:name="{}"]'.format(feature)
        items = self.root.findall(query, AndroidManifest.XMLNS)
        return bool(items)

    def add_feature(self, feature, required=True):
        if self.has_feature(feature):
            log.info("Manifest already has the feature: {}".format(feature))
            return
        item = ElementTree.SubElement(self.root, 'uses-feature', {
            'android:name': feature,
            'android:required': 'true' if required else 'false'
        })
        item.tail = '\n'
        log.debug("feature {} was added".format(feature))

    def has_permission(self, perm):
        query = './uses-permission[@android:name="{}"]'.format(perm)
        items = self.root.findall(query, AndroidManifest.XMLNS)
        return bool(items)

    def add_permission(self, perm):
        if self.has_permission(perm):
            log.info("Manifest already has the permission: {}".format(perm))
            return
        item = ElementTree.SubElement(self.root, 'uses-permission', {
            'name': perm
        })
        item.tail = '\n'
        log.debug("permission {} was added".format(perm))

    def save(self, path):
        self.tree.write(path)
