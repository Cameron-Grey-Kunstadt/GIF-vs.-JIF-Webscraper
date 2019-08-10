#Cameron Kunstadt
# 8/1/2019
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

definitionLinks = []  # list of all the links
gCounter = 0  # counting up words with the 'g' pronunciation
jCounter = 0  # counting up words with the 'j' pronunciation

def PronunciationGrabber(individualDefiniton):
    #  this method opens up the individual definition page link, finds the pronunciation guide, and determines
    #  which sound it has, and increments its respective counter
    if " " not in individualDefiniton.attrs['href']:
        #  definitions with spaces have different urls, and most often do not have pron. guides, and can be ignored
        if "\\" in str(individualDefiniton.encode('utf-8')):
            # if, when converted to unicode, the word contains a '\', it is a special non-ASCII character
            # and for these purposes can be be ignored
            print("Unreadable Character")
            return 0
        print(individualDefiniton)
        defPage = urlopen("https://www.merriam-webster.com" + str(individualDefiniton.attrs['href']))
        pageObj = BeautifulSoup(defPage, "html.parser")
        print(pageObj.find("span", {"class": "pr"}))
        if pageObj.find("span", {"class": "pr"}) is not None:
            encodedPronun = (str(pageObj.find("span", {"class": "pr"})))
            if 'j' in encodedPronun:
                return 2
            if 'g' in encodedPronun:
                return 1
        else:
            print("NO IPA")
            return 0
    else:
        print("NO IPA")
        return 0


def GetLocalLinks(currentSite):
    # gets all the links on the page, adds them to list
    html = urlopen(currentSite)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.findAll("a", href=re.compile("^(/dictionary/)((?!:).)*$")):
            definitionLinks.append(link)
            print(link)


def PageShifter(startingSite):
    ourPage = (startingSite + "/")
    #setting up the link to accept a num at the end
    for pageNum in range(1, 44):
        ourPage = ourPage+str(pageNum)
        #adding the num at the end to turn pages
        print(ourPage)
        GetLocalLinks(ourPage)
        #grabbing the links on every page
        ourPage = (startingSite + "/")
        #setting it back to take the number off



PageShifter("https://www.merriam-webster.com/browse/dictionary/g")

for links in definitionLinks[0:]:
    if PronunciationGrabber(links) == 1:
        gCounter += 1
        print("gCounter is: " + str(gCounter))
    if PronunciationGrabber(links) == 2:
        jCounter += 1
        print("jCounter is: " + str(jCounter))

print("gCounter is: " + str(gCounter))
print("jCounter is: " + str(jCounter))

if gCounter > jCounter:
    print("SEE, ITS GIF")
else:
    print("ok fine, i guess it's jif")

