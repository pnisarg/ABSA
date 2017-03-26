import xml.etree.ElementTree as ET
import sys
import codecs

def convertXMLtoCsv(root):
    ofile = codecs.open('result.csv', 'wb', encoding='utf8')
    for sentence in root.getchildren():
        aspectCategory = ''
        aspectPolarity = ''
        id = sentence.attrib['id']
        polarity = sentence.attrib['polarity']
        text = sentence.getchildren()[0].text
        if len(sentence.getchildren()) > 1:
            aspectCategory = sentence.getchildren()[1].getchildren()[0].attrib['category']
            aspectPolarity = sentence.getchildren()[1].getchildren()[0].attrib['polarity']
        ostring = id + "#"+ polarity + "#" + text + "#" + aspectCategory + "#" + aspectPolarity + "\n"
        ofile.write(ostring) 
    ofile.close()


def main():
    root = ET.parse(sys.argv[1]).getroot()
    convertXMLtoCsv(root)

if __name__ == '__main__':
    main()

