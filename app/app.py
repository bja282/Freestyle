import code
from urllib.request import urlopen
from IPython import embed
from bs4 import *

#Program-wide variables.
url = 'http://web.mta.info/status/serviceStatus.txt'
response = urlopen(url)
soup = BeautifulSoup(response, 'lxml-xml')
lines = []
xml_tags = soup.find_all('line')

#Parse the MTA current services.
def parser():
    for tag in xml_tags:
        line = {
            "name": tag.find('name').string,
            "status": tag.find('status').string,
            "date": tag.find('Date').string,
            "time": tag.find('Time').string,
            "desc": BeautifulSoup(tag.find('text').prettify(formatter=None), 'lxml'),
            "announcements": "",
            "type": ""
        }
        lines.append(line)
parser()
#Parse through MTA descriptions - just extract text relevant to service changes.
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

#Parse through train lines and identify line type (subway, rail, bridge/tunnel, or bus)
def typeparse(line):
    matches = []
    for line in lines:
        if line["name"].lower() in  line.upper():
            matches.append(line)

#List all lines: subways, trains (LIRR, MetroNorth), buses, and bridges/tunnels
def listlines():
    print("Below is a list of all subway, rail, bus and bridge and tunnel services operated by the MTA.")
    for line in lines:
        soupertrain(line)
        print("+", line['name']+", Service Status: "+line['status'])#+" "+line['desc'])
    print('''
    To view this list again at any time, enter \"list\" into the prompt.
    To exit this program at any time, enter \"done\" into the prompt.\n''')
listlines()

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
def menu():
    while True:
        try:
            service_prompt = input("Please enter the name of an MTA service to review its current service status: ")
            if service_prompt.lower() == "done":
                break
            if service_prompt.lower() == "interact":
                embed()
            if service_prompt.lower() == "list":
                listlines()
                menu()
            if service_prompt.lower() != "done":
                line_lookup(service_prompt)
            else:
                break
        except(IndexError, ValueError):
            print("\nSorry, didn't recognize that. Try again?\n")

menu()
