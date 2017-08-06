import code
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
        "date": tag.find('Date').string,
        "time": tag.find('Time').string,
        "desc": BeautifulSoup(tag.find('text').prettify(formatter=None), 'lxml'),
        "announcements": ""
    }
    lines.append(line)

#Text parser - just looking to extract the service changes and leave behind HTML
def soupertrain(bowl):
    paprika = []
    if bowl['status'].lower() != "Good Service".lower():
        try:
            leansoup = bowl['desc'].find_all('a')
            if bowl['status'].lower() == "delays":
                try:
                    paprika.append("The "+bowl['name']+" line is currently running with delays.")
                except:
                    pass
            for x in range(0, len(leansoup)):
                if leansoup[x].has_attr('class') and leansoup[x].has_attr('onclick'):
                    paprika.append(leansoup[x].text)
        except(ValueError, IndexError):
            pass
    elif bowl['status'].lower() == "delays":
        try:
            paprika.append("The "+bowl['name']+" line is currently running with delays.")
        except:
            pass
    else:
        paprika.append(bowl['status'].title())
    bowl['announcements']=paprika

for line in lines:
    soupertrain(line)
    print("+", line['name']+", Service Status: "+line['status'])#+" "+line['desc'])

def numberofchanges(announcements):
    count = 0

    if count>0:
        print(str(count))
    else:
        print("No current service changes or updates.")

def countcheck(count):
    if count>0 and count<2:
        return(str(count)+" current service change or update.")
    elif count>1:
        return(str(count)+" current service changes or updates.")
    else:
        return("No current service changes or updates.")

def line_lookup(name):
  matches = []
  count = 0
  for line in lines:
      if line["name"].upper() == name.upper():
          matches.append(line)
  if matches[0]['announcements'][0].lower() == "good service".lower():
      count = 0
  else:
      count=len(matches[0]['announcements'])
  #code.interact(local=locals())
  print("\n\nLine: "+matches[0]["name"]+"\n"+"Service Status: "+countcheck(count))
  try:
      for match in matches[0]["announcements"]:
          if count>0:
              print ("+ ", match)
          else: pass
  except(ValueError, IndexError):
      pass
  print("\n")


#MENU
while True:
    try:
        service_prompt = input("Please enter the name of an MTA service to review its current service status: ")
        if service_prompt.lower() == "interact":
            code.interact(local=locals())
        if service_prompt.lower() != "done":
            line_lookup(service_prompt)
        else:
            break
    except(IndexError, ValueError):
        service_prompt = input("Sorry, didn't recognize that. Try again? ")
        if service_prompt != "done":
            line_lookup(service_prompt)
        else:
            service_prompt = input("Sorry, didn't recognize that. Try again? ")
            if service_prompt != "done":
                line_lookup(service_prompt)
