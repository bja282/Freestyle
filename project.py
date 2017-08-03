from urllib.request import urlopen
from bs4 import *

url = 'http://web.mta.info/status/serviceStatus.txt'
response = urlopen(url)
soup = BeautifulSoup(response, 'lxml-xml')

lines = []

xml_tags = soup.find_all('line')

for tag in xml_tags:
    line = {
        "name": tag.find('name').string,
        "status": tag.find('status').string,
        "desc": tag.find('text').string
    }
    lines.append(line)

for line in lines:
     print("+", line['name']+", Service Status: "+line['status'])#+" "+line['desc'])

while True:
    service_prompt = input("Please enter the name of an MTA service to review its current service status: ")
    if service_prompt == "123":
        print(lines[0]['desc'])
    if service_prompt == "done":
        break
