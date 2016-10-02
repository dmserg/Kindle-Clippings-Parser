import dicttoxml

if __name__ == '__main__':
    from sys import argv
    from ClippingsParser import ClippingsParser
    cp = ClippingsParser()
    result = cp.parseClippings(argv[1])

    xml = dicttoxml.dicttoxml(result)
    xml = xml[:xml.index("?>")+2] + '<?xml-stylesheet type="text/xsl" href="clippings.xsl" ?>' + xml[xml.index("?>")+2:]
    print(xml)