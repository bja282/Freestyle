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

# the long way
def line_lookup(name):
  matches = []
  for line in lines:
      if line["name"].upper() == name.upper():
          matches.append(line)
  print("Line: "+matches[0]["name"]+"\n"+"Service Status: ",matches[0]["desc"])


while True:
    try:
        service_prompt = input("Please enter the name of an MTA service to review its current service status: ")
        if service_prompt != "done":
            line_lookup(service_prompt)
        else:
            break
    except(IndexError, ValueError):
        service_prompt = input("Sorry, didn't recognize that. Try again? ")
        if service_prompt != "done":
            line_lookup(service_prompt)
        else:
            break
