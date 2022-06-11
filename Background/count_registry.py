import ssl
import urllib.request
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context
def getHtml(url):
	html = urllib.request.urlopen(url).read()
	html = html.decode('utf8').replace('\n', '').replace('\r', '')
	re_format = re.compile('<!--[^>]*-->')
	html = re_format.sub('', html)
	return html

url = 'https://opentelemetry.io/registry/?s=&component=all&language=all'

bs = BeautifulSoup(getHtml(url).encode('utf8'), "html.parser")


languages = bs.find_all("a", "dropdown-item", id = re.compile('language-item'))
components = bs.find_all("a", "dropdown-item", id = re.compile('component-item'))

languages_row = []
components_col = []

languages_lenth = len(languages)
components_lenth = len(components)  

table = [[] for k in range(components_lenth+1)]

for i in range(languages_lenth): 
	for j in range(components_lenth):
		if bs.find_all(attrs={"data-registrylanguage":languages[i].attrs['value'], "data-registrytype":components[j].attrs['value']}) != None:
			#print(len(bs.find_all(attrs={"data-registrylanguage":languages[i].attrs['value'], "data-registrytype":components[j].attrs['value']})))
			table[j].append(len(bs.find_all(attrs={"data-registrylanguage":languages[i].attrs['value'], "data-registrytype":components[j].attrs['value']})))
		else:
			#print(0)
			table[j].append(0)
	languages_row.append(languages[i].get_text())

for m in range(languages_lenth):
	table[j+1].append(len(bs.find_all(attrs={"data-registrylanguage":languages[m].attrs['value']})))

table[j+1].append(len(bs.find_all("li", "media")))

for n in range(components_lenth):
	table[n].append(len(bs.find_all(attrs={"data-registrytype":components[n].attrs['value']})))
	components_col.append(components[n].get_text())


languages_row.append('sum')
components_col.append('sum')

#draw the table
plt.figure(figsize = (20,8))
tab = plt.table(cellText=table, colLabels=languages_row, rowLabels=components_col, loc="center")
tab.scale(1,2)
plt.axis('off')
plt.show()


print("success!")