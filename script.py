from lxml.etree import parse
import json

prefix = {'dc': 'http://purl.org/dc/elements/1.1/',
 'srw': 'http://www.loc.gov/zing/srw/',
 'srw_dc': 'info:srw/schema/1/dc-schema',
 'xsi': 'http://www.w3.org/2001/XMLSchema'}

steps = 1000
url = "http://www.lexml.gov.br/busca/SRU?operation=searchRetrieve&query=urn+=%22federal%22&maximumRecords="+str(steps)+"&startRecord="
numberOfRecords = 1+steps

def get_laws(restart=False, startRecord=0, numberOfRecords=numberOfRecords):
    #log = open('laws.log', 'a')
    soup = parse(url+str(startRecord))
    lastRecord = startRecord + steps
    if startRecord == 0:
        numberOfRecords = int(soup.xpath("//srw:numberOfRecords", namespaces=prefix)[0].text)
        lawjson = open('laws.json', 'w')
        lawjson.write(json.dumps([]))
        lawjson.close()
        print "Total results: "+ str(numberOfRecords)
    print "Getting from " + str(startRecord) + " to " + str(lastRecord)

    tmp_f = open('laws.json', 'r')
    tmp = json.loads(tmp_f.read())
    tmp_f.close()

    laws = []
    for l in soup.xpath("//srw:record", namespaces=prefix):
        law = {}
        law['title'] = l.xpath("srw:recordData/srw_dc:dc/dc:title", namespaces=prefix)[0].text
        law['urn'] = l.xpath("srw:recordData/srw_dc:dc/urn", namespaces=prefix)[0].text
        law['date'] = l.xpath("srw:recordData/srw_dc:dc/dc:date", namespaces=prefix)[0].text
        law['description'] = l.xpath("srw:recordData/srw_dc:dc/dc:description", namespaces=prefix)[0].text
        laws.append(law)

    lawjson = open('laws.json', 'w')
    
    if restart:
        numberOfRecords = int(soup.xpath("//srw:numberOfRecords", namespaces=prefix)[0].text)
        pops = []
        diff_laws = []
        for old_law in tmp[-1*steps:]:
            for index, new_law in enumerate(laws):
                if old_law['urn'] == new_law['urn']:
                    pops.append(new_law)
                    print "Pop!"
        for new_law in laws:
            if new_law not in pops:
                diff_laws.append(new_law)
        laws = diff_laws
        restart = False

    lawjson.write(json.dumps(tmp+laws, indent=4))
    lawjson.close()
    l2 = open('laws'+str(startRecord)+'.json', 'w')
    l2.write(json.dumps(tmp+laws, indent=4))
    l2.close()
    #log.close()
    if lastRecord <= numberOfRecords:
        get_laws(restart, lastRecord, numberOfRecords)
