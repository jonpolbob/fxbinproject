from lxml import html
from lxml import etree
import requests

#programme de test de la lecture des paires en live

page = requests.get('https://www.dailyfx.com/forex-rates')
#for e in page:
#    print(e)
text_file = open(r"c:\tmp\Output.txt", "wb")
text_file.write(page.content)
text_file.close()

tree = html.fromstring(page.content)


#eurusdvalue = tree.xpath('//tr[@id="EURUSD"]') #execute une instruction xpath pour trouve le truc
#lestd = eurusdvalue[0].xpath('//td/b/span[@id="eurusd-priceBid"]')
eurusdvalue2=None
eurusdvalue = tree.xpath('//div')
for e in eurusdvalue:
    if ('class' in e.attrib):
        if (e.attrib['class'] == 'col-sm-6'):
            eurusdvalue2 = e.xpath('//table/tbody/tr')#    print (e.attrib)
            break

eurusdvalue3 = None

if (eurusdvalue2 != None):
    for e in eurusdvalue2:
        if ('id' in e.attrib):
            if e.attrib['id'] == 'EURUSD0':
                #print(e.attrib['id'])
                eurusdvalue3= e.xpath('//td/a/div')

eurusdvalue4 = None

if (eurusdvalue3 != None):
    for e in eurusdvalue3:
        eurusdvalue4 = eurusdvalue3.xpath('//div/div')
        for z in eurusdvalue4:
            if 'id' in z.attrib:
                print(z.attrib['id'])
                if ('priceLow' in z.attrib['id']):
                    print(z.attrib['id'][:6],':',z.text)
                    print (z.xPath("//text()"))

                #if (e.attrib['class'] == 'container'):
                #eurusdvalue2 = e.xpath('//tr')  # print (e.attrib)

        #print (e.attrib)

usdjpyvalue = tree.xpath('//tr[@id="USDJPY"]')
print(usdjpyvalue)



