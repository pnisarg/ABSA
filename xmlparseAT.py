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
            aspectTerms = sentence.find('aspectTerms')
            for aspectTerm in aspectTerms.getchildren():
                afrom = afrom + "&"+ aspectTerm.attrib['from']
                ato = ato +"&"+aspectTerm.attrib['to']
                apolarity = apolarity + "&" +aspectTerm.attrib['polarity']
                aterm = aterm +"&"+ aspectTerm.attrib['term']
        ostring = id + "#" + text + "#" + afrom[1:] + "#" + ato[1:] + "#" + apolarity[1:] + "#" + aterm[1:] + "\n"
        ofile.write(ostring) 
    ofile.close()


def main():
    root = ET.parse(sys.argv[1]).getroot()
    convertXMLtoCsv(root)

if __name__ == '__main__':
    main()

