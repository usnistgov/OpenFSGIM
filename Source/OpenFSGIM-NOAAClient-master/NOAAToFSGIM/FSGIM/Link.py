import xml.etree.ElementTree as ET

class Link:

    @staticmethod
    def createLinks(rootElement, links):
        for link in links:
            linkChildElement = Link.createLink(link[0], link[1])
            rootElement.append(linkChildElement)
        return rootElement

    @staticmethod
    def createLink(relation,uri):
        link = ET.Element("link" )
        link.attrib["rel"] = str(relation)
        link.attrib["href"] = str(uri)
        return link

