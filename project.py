from urllib.request import urlopen
from bs4 import *

# for tag in soup.find_all(re.compile("^name")):
#      print(tag)
#
# for tag in soup.find_all('name'):
#      tag.string

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

#print(lines)

for line in lines:
     print("+", line['name']+", Service Status: "+line['status'])#+" "+line['desc'])

while x == True:
    service_prompt = input("Please enter the name of an MTA service to review its current service status: ")
    if service_prompt == "123":
        print(line[0])
