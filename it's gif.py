# Cameron Kunstadt
# 8/1/2019
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

definitionLinks = []  # list of all the links
gCounter = 0  # counting up words with the 'g' pronunciation
jCounter = 0  # counting up words with the 'j' pronunciation


def pronunciation_grabber(individual_definition):
    #  this method opens up the individual definition page link, finds the pronunciation guide, and determines
    #  which sound it has, and increments its respective counter
    if " " not in individual_definition.attrs['href']:
        #  definitions with spaces have different urls, and most often do not have pron. guides, and can be ignored
        if "\\" in str(individual_definition.encode('utf-8')):
            # if, when converted to unicode, the word contains a '\', it is a special non-ASCII character
            # and for these purposes can be be ignored
            print("Unreadable Character")
            return 0
        print(individual_definition)
        def_page = urlopen("https://www.merriam-webster.com" + str(individual_definition.attrs['href']))
        page_obj = BeautifulSoup(def_page, "html.parser")
        print(page_obj.find("span", {"class": "pr"}))
        if page_obj.find("span", {"class": "pr"}) is not None:
            pronunciation = (str(page_obj.find("span", {"class": "pr"})))
            if 'j' in pronunciation:
                return 2
            if 'g' in pronunciation:
                return 1
        else:
            print("NO IPA")
            return 0
    else:
        print("NO IPA")
        return 0


def get_local_links(current_site):
    # gets all the links on the page, adds them to list
    html = urlopen(current_site)
    bs_obj = BeautifulSoup(html, "html.parser")
    for link in bs_obj.findAll("a", href=re.compile("^(/dictionary/)((?!:).)*$")):
            definitionLinks.append(link)
            print(link)


def page_shifter(starting_site):
    our_page = (starting_site + "/")
    # setting up the link to accept a num at the end
    for pageNum in range(1, 44):
        our_page = our_page+str(pageNum)
        # adding the num at the end to turn pages
        print(our_page)
        get_local_links(our_page)
        # grabbing the links on every page
        our_page = (starting_site + "/")
        # setting it back to take the number off


page_shifter("https://www.merriam-webster.com/browse/dictionary/g")

for links in definitionLinks[0:]:
    if pronunciation_grabber(links) == 1:
        gCounter += 1
        print("gCounter is: " + str(gCounter))
    if pronunciation_grabber(links) == 2:
        jCounter += 1
        print("jCounter is: " + str(jCounter))

print("gCounter is: " + str(gCounter))
print("jCounter is: " + str(jCounter))

if gCounter > jCounter:
    print("SEE, ITS GIF")
else:
    print("ok fine, i guess it's jif")


