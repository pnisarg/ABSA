import xml.etree.ElementTree as ET
import sys
import codecs

def convertXMLtoCsv(root):
    ofile = codecs.open('result.csv', 'wb', encoding='utf8')
    for sentence in root.getchildren():
        afrom = ''
        ato = ''
        apolarity = ''
        aterm = ''
        id = sentence.attrib['id']
        text = sentence.getchildren()[0].text
        if len(sentence.getchildren()) > 1:
            afrom = sentence.getchildren()[1].getchildren()[0].attrib['from']
            ato = sentence.getchildren()[1].getchildren()[0].attrib['to']
            apolarity = sentence.getchildren()[1].getchildren()[0].attrib['polarity']
            aterm = sentence.getchildren()[1].getchildren()[0].attrib['term']
        ostring = id + "#" + text + "#" + afrom + "#" + ato + "#" + apolarity + "#" + aterm + "\n"
        ofile.write(ostring) 
    ofile.close()


def main():
    root = ET.parse(sys.argv[1]).getroot()
    convertXMLtoCsv(root)

if __name__ == '__main__':
    main()

