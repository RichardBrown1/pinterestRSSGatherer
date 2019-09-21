from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal
from pytz import timezone
import urllib
import urllib.request
import sys

if len(sys.argv)==1:
	print("Usage: " + sys.argv[0] + " outputFileName username [collection]")
	print("If collection is not specified feed.rss which is last 25 items overall will be used")
	sys.exit("Please specify username")

#execution time counter	
#startTime = datetime.now(tz=None)
#print("START: " + str(startTime))

#make an argument parser to input usernames and file names
filename = sys.argv[1] + ".html"
username = sys.argv[2]

for x in sys.argv:
	if x == 0:
		x += 2
		
	if len(sys.argv) == 3:
		location = "feed"
	else:
		location = sys.argv[x]
	
	url = "https://www.pinterest.com/" + username + "/" + location + ".rss"

	htmlFile = open(filename, "w", encoding="utf-8")

	#Prep Soup
	content = urllib.request.urlopen(url)
	soup = BeautifulSoup(content,"html5lib",from_encoding="utf-8")

	timedateformat = "%a, %d %b %Y %I:%M:%S %Z"

	#Functions
	def tzOption():
		#Make an option to add in timezone through an argument parser
		placeholder = 123

	def tzConvert(timeDate):
		#timeDateObj = datetime.strptime(timeDate, "%a, %d %b %Y %I:%M:%S %Z")
		timeDateObj = parse(timeDate)
		timeDateObjLocal = timeDateObj.astimezone(tzlocal())
		timeDateStr = timeDateObjLocal.strftime(timedateformat)
		return timeDateStr

	#Store in lists
	titles = soup.find_all("title")
	links = soup.find_all("link")
	descriptions = soup.find_all("description")
	pubDates = soup.find_all("pubdate")
	guids = soup.find_all("guid")

	#print(titles)
	#print(links)

	#HTML File Head
	htmlFile.write("<head>")
	htmlFile.write("<title>" + username + "'s Pinterest Data </title>")
	htmlFile.write("<link rel='stylesheet' type='text/css' href='style.css'")
	htmlFile.write("</head>")

	#HTML File Body
	htmlFile.write("<body>")
	htmlFile.write("<h1>" + "Display Name: " + titles[0].text + " - Username: " + username + "</h1>")
	htmlFile.write("<h3> Updated: " + tzConvert(soup.find("lastbuilddate").text) + "</h3>")

	htmlFile.write("<div id='content'>")
	for i in range(len(soup.find_all("item"))):
		#print(i)
		htmlFile.write("<div class='item'>")
		htmlFile.write("<h2 class='timestamp'>" + tzConvert(pubDates[i].text) + "</h3>")
		htmlFile.write(descriptions[i+1].text)
		#htmlFile.write("<h3 class='title'>" + (titles[i+1].text) + "</h2>")
		htmlFile.write("</div>")

	htmlFile.write("</body>")
	
	
#endTime = datetime.now(tz=None)
#print("END - Took: " + str(endTime-startTime))
