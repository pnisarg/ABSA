import xml.etree.ElementTree as ET
import sys
import codecs

def convertXMLtoCsv(root, outputPath):
    ofile = codecs.open(outputPath, 'wb', encoding='utf8')
    for sentence in root.getchildren():
    aspectCategory = ''
        aspectPolarity = ''
        id = sentence.attrib['id']
        polarity = sentence.attrib['polarity']
        text = sentence.getchildren()[0].text
        if len(sentence.getchildren()) > 1:
            aspectCategories = sentence.find('aspectCategories')
            for AC in aspectCategories.getchildren():
                aspectCategory = aspectCategory + "&" + AC.attrib['category']
                aspectPolarity = aspectPolarity + "&" + AC.attrib['polarity']
        ostring = id + "#"+ polarity + "#" + text + "#" + aspectCategory[1:] + "#" + aspectPolarity[1:] + "\n"
        ofile.write(ostring) 
    ofile.close()


def main():
    root = ET.parse(sys.argv[1]).getroot()
    convertXMLtoCsv(root, sys.argv[2])

if __name__ == '__main__':
    main()

