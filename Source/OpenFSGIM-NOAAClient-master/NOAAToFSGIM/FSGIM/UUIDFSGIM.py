import hashlib
import xml.etree.ElementTree as ET
import uuid


class UuidFSGIM(object):

    @staticmethod
    def createUuid(Uuid):
        Id = ET.Element("id")
        Id.text = "urn:uuid:"+str(Uuid)
        return Id

    @staticmethod
    def generate(namespace, name):
        return str(uuid.uuid5(namespace,name))



