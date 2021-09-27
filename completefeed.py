#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
import lxml
import glob
import re
import sys


path="feedcopies/websites/**/podcast*"
items = []
found_already = set()
tritons = {}

files = sorted(glob.iglob("feedcopies/websites/www.npr.org/**/podcast*", recursive=True))
files += sorted(glob.iglob("feedcopies/websites/feeds.npr.org/**/podcast*", recursive=True))

print("Found files, now parsing", file=sys.stderr)

def getFilename(item):
    enc = item.enclosure['url']
    url = urlparse(enc)
    filename = re.sub(r'.*/', '', url.path)
    filename = re.sub(r'-[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', '', filename) 
    return filename


for xmlpath in reversed(files):
    with open(xmlpath, "r") as xmlfile:
        text = "".join(xmlfile.readlines())
        soup = bs(text, "lxml-xml")
        for item in soup.find_all('item'):
            if (item.enclosure is None 
                    or "worddocument" in str(item)
                    or "officedocumentsettings" in str(item)
                    or "</o:p>" in str(item)):
                continue
            filename = getFilename(item)
            if (re.match(r'^\s*$', filename)):
                #print("Filename extractor had trouble with URL of "+item.title.string, file=sys.stderr)
                continue

            guidkey = "GUID: "+item.guid.string
            titlekey = "Title: "+item.title.string

            if (guidkey in found_already):
                continue
            if ("tritondigital" in item.enclosure['url']):
                # Hold out hope for a different copy first
                tritons[guidkey] = item
                continue
            elif (guidkey in tritons):
                # Yes, our hope has come true, we'll take this one and toss
                # the Triton
                tritons.pop(guidkey)
            print(guidkey, file=sys.stderr)
            items.append(item)
            found_already.add(guidkey)

print("Done parsing, now sorting", file=sys.stderr)

def getDate(item):
    return mktime_tz(parsedate_tz(item.pubDate.string))

items = sorted(items, key=getDate)

for item in items:
    print(item)

for filename in tritons:
    print("Couldn't find a non-triton entry for one instance of title "+item.title.string+", date "+item.pubDate.string, file=sys.stderr)
