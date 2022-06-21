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

dynamicurl = '/orgs/opentracing-contrib/repositories?page=1'
root = 'https://github.com'
url = root + dynamicurl



bs = BeautifulSoup(getHtml(url).encode('utf8'), "html.parser")
languages = bs.find_all(attrs={"class":"SelectMenu-item", "aria-checked":"false"})
languages_lenth = len(languages)
languages_row = []


for i in range(languages_lenth):
	if languages[i].find('input')["name"] == "language" :
		languages_row.append(languages[i].get_text().strip())

count_lenth = len(languages_row)
count = [0]*(count_lenth+1)

sum = 0
while bs.find('div', attrs={"role":"navigation"}).find('a', attrs={"rel":"next"}):
	dynamicurl = bs.find('div', attrs={"role":"navigation"}).find('a', attrs={"rel":"next"})["href"] 
	url = root + dynamicurl
	repositories = bs.find_all('span', attrs={"itemprop":"programmingLanguage"})
	repositories_lenth = len(repositories)
	for j in range(count_lenth):
		temp = 0
		for k in range(repositories_lenth):
			if repositories[k].get_text() == languages_row[j]:
				temp = temp + 1
				sum = sum + 1
		count[j] = count[j] + temp
	bs = BeautifulSoup(getHtml(url).encode('utf8'), "html.parser")

repositories = bs.find_all('span', attrs={"itemprop":"programmingLanguage"})
repositories_lenth = len(repositories)
for j in range(count_lenth):
	temp = 0
	for k in range(repositories_lenth):
		if repositories[k].get_text() == languages_row[j]:
			temp = temp + 1
			sum = sum + 1
	count[j] = count[j] + temp


languages_row.append("Sum")
count[j+1] = sum

#print(languages_row)
#print(count)
col = ["Temp"]
table = [count]

#draw the table
plt.figure(figsize = (20,8))
tab = plt.table(cellText=table, colLabels=languages_row, rowLabels=col, loc="center", cellLoc="left")
tab.scale(1,2)
plt.axis('off')
plt.show()

print("success!")