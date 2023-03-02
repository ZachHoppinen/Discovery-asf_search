import xml.etree.ElementTree as ETree
from asf_search.export.export_translators import ASFSearchResults_to_properties_list

class XMLStreamArray(list):
    def __init__(self, results):
        self.pages = results
        self.len = 1
        self.header = """<?xml version="1.0"?><metalink xmlns="http://www.metalinker.org/" version="3.0">
        <publisher><name>Alaska Satellite Facility</name><url>http://www.asf.alaska.edu/</url></publisher>
        <files>"""

        self.footer = "</files>\n</metalink>"

    def get_additional_fields(self, product):
        return {}
    
    def __iter__(self):
        return self.streamPages()

    def __len__(self):
        return self.len

    def streamPages(self):
        yield self.header
        for page in self.pages:
            properties_list = ASFSearchResults_to_properties_list(page, self.get_additional_fields)
            yield [self.getItem(p) for p in properties_list]
        
        yield self.footer

    def getItem(self, p):
        file = ETree.Element("file", attrib={'name': p['fileName']})
        resources = ETree.Element('resources')

        url = ETree.Element('url', attrib={'type': 'http'})
        url.text = p['url']
        resources.append(url)
        file.append(resources)
        
        if p['md5sum'] and p['md5sum'] != 'NA':
            verification = ETree.Element('verification')
            h = ETree.Element('hash', {'type': 'md5'})
            h.text = p['md5sum']
            verification.append(h)
            file.append(verification)
            
        if p['bytes'] and p['bytes'] != 'NA':
            size = ETree.Element('size')
            size.text = str(p['bytes'])
            file.append(size)
        
        return '\n' + ETree.tostring(file, encoding='unicode')

    def indent(self, elem, level=0):
        # Only Python 3.9+ has a built-in indent function for element tree.
        # https://stackoverflow.com/a/33956544
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i