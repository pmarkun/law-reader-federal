from lxml import html
import json, urllib2, html2text

lawjson = open('laws.json', 'r')
laws = json.loads(lawjson.read())
lawjson.close()

def getCamaraUrl(l):
    if not l.has_key('url'):
        print 'Getting ' + l['title']
        url = 'http://www.lexml.gov.br/urn/' + l['urn']
        soup = urllib2.urlopen(url)
        soup = html.parse(url).getroot()
        new_url = soup.xpath('//a[starts-with(@href, "http://www2.camara.gov.br/")][contains(@href, "publicacaooriginal")]')
        if len(new_url) > 0:
            l['url'] = new_url[0].get('href')
    return l
 
def getCamaraText(l):
    if l.has_key('url') and not l.has_key('text'):
        print "Getting text from " + l['title']
        soup = urllib2.urlopen(l['url'])
        soup = html.parse(soup).getroot()
        l['raw'] = html.tostring(soup.xpath('//div[@class="textoNorma"]/div[@class="texto"]')[0])
        l['text'] = html2text.html2text(l['raw'])
        filename = 'data/' + l['urn'].split(';')[0][:-6]+'::'+l['urn'].split(';')[1] + '.json'
        jason = open(filename, 'w')
        jason.write(json.dumps(l, indent=4))
        jason.close()

def getBulkUrls(steps=1000):
    i = 0
    print "Getting " + str(steps)
    for index, l in enumerate(laws):
        if i <= steps:
            if not l.has_key('url'): #only count when not url
                laws[index] = getCamaraUrl(l)
                i += 1
        else:
            laws[index] = getCamaraUrl(l)
            print "Updating json..."
            lawjson = open('laws.json', 'w')
            lawjson.write(json.dumps(laws, indent=4))
            lawjson.close()
            i = 0
            print "Getting " + str(steps)

def getBulkTexts():
    for index, l in enumerate(laws[0:3]):
        getCamaraText(l)