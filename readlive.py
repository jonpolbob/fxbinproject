from lxml import html
from lxml import etree
import requests

page = requests.get('https://www.dailyfx.com/forex-rates')
tree = html.fromstring(page.content)

eurusdvalue = tree.xpath('//tr[@id="EURUSD"]') #execute une instruction xpath pour trouve le truc
eurusdchild = eurusdvalue.getchildren()
print(eurusdchild)

usdjpyvalue = tree.xpath('//tr[@id="USDJPY"]')
print(usdjpyvalue)



