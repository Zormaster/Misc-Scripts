import requests
from bs4 import BeautifulSoup

url = input("Enter URL: ")
response = requests.get(url).text

soup = BeautifulSoup(response, 'html.parser')

links = []

for link in soup.find_all('a', href = True):

# Failed attempts

#    link.get('href')
#    if link.get('href') != '':
#        link = re.search('".*://.*"', link.text)
#        if('://' not in link.get('href')):
#            link = '{}{}'.format(url, link.get('href'))
#        if not (link.endswith('mp4')):
    if '://' in link['href']:
        links.append(link['href'])
for link in soup.find_all('link', href = True):
    if '://' in link['href']:
        links.append(link['href'])
for link in links:
    print(link)