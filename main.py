import sys, string

from xml.sax import saxutils, handler, make_parser


class ContentGenerator(handler.ContentHandler):

    def __init__(self, out=sys.stdout):
        handler.ContentHandler.__init__(self)
        self.requirement = ""
        self.testcaseid=""
        self.result=""
        self.currenttag=""

    def startDocument(self):
        print('start')

    def startElement(self, name, attrs):
        print('start', name)
        self.currenttag=name
        for attr_name, value in attrs.items():
            print (attr_name, value)

    def endElement(self, name):
        print ('end', name)
        self.currenttag=""
        if name == "TestCase":
            print("requirement id:{} test caseid is:{} result is :{}",self.requirement,self.testcaseid,self.result)
            self.requirement = ""
            self.testcaseid = ""
            self.result = ""
            self.currenttag = ""


    def characters(self, content):
        print("self.currenttag is",self.currenttag)
        if self.currenttag == "requirementID":
            self.requirement = content
        elif self.currenttag == "testCaseID":
            self.testcaseid = content
        elif self.currenttag == "result":
            if(len(self.requirement)>0):
                self.result = content
        #print (content)

    def ignorableWhitespace(self, content):
        print ('whitespace', '"', content, '"')

    def processingInstruction(self, target, data):
        print ('processing instruction', target, data)


if __name__ == '__main__':
    parser = make_parser()
    parser.setContentHandler(ContentGenerator())
    parser.parse(sys.argv[1])