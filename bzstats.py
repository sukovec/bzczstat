#!/usr/bin/env python3

from urllib.request import urlopen
import pickle
import os
import datetime
from bs4 import BeautifulSoup

# Song order file - file with song orders in graph (order on web can change over time)
bandurl = "http://bandzone.cz/vetryslecnypetry"
sofile = "bzstat/sorder.st"
datfile = "bzstat/data.dat"

# de-serialize saved stats and orders
if not os.path.exists(sofile): # create it
    cfg = {"cpos": 0, "songsort": {}, "laststat": {}}
    with open(sofile, "wb") as wrto:
        pickle.dump(cfg, wrto)
else: # load 
    with open(sofile, "rb") as rdfile:
        cfg = pickle.load(rdfile)

# download stats from webpage
resp = urlopen(bandurl)
soup = BeautifulSoup(resp.read(), 'html.parser') # parse 

sorted_counts = {}
sorted_names = {}

for song in soup.findAll("li", {"itemprop": "track"}):
    # get stats in page
    songname = song.find("strong", {"class": "title", "itemprop": "name"}).string.strip()
    count = song.find("meta", {"itemprop": "interactionCount"})["content"].split(":")[1]
    count = int(count)

    
    if songname in cfg["songsort"]: # if song appeared before (pretty expected)
        sorted_counts[cfg["songsort"][songname]] = count - cfg["laststat"][songname] # get difference between last and now
        sorted_names[cfg["songsort"][songname]] = songname
        cfg["laststat"][songname] = count # save now
    else: # song is found for first time
        sorted_counts[cfg["cpos"]] = 0
        sorted_names[cfg["cpos"]] = songname
        cfg["songsort"][songname] = cfg["cpos"]
        cfg["laststat"][songname] = count
        cfg["cpos"] = cfg["cpos"] + 1

with open(sofile, "wb") as wrto:
    pickle.dump(cfg, wrto)


arr = [ datetime.date.today() ]
#gplot = "set terminal png size 1024,768\n""
gplot = "set terminal svg size 1000,1000\n"
gplot += "set encoding utf8\n"
#gplot += "set timefmt '%m/%d/%y'\n"
#gplot += 'set xrange ["03/21/95":"03/22/95"]\n'
#gplot += "set format x '%m/%d'\n"
gplot += "plot "


for i in range(cfg["cpos"]):
    if not i in sorted_counts:
        arr.append("")
    else:
        arr.append(sorted_counts[i])
    
    if i != 0:
        gplot += ", "
    gplot += "'" + datfile + "' using " + str(i + 2) + " title '" + sorted_names[i] + "' with lines"



with open(datfile, "a") as writefile:
    writefile.write(", ".join(map(str, arr)))
    writefile.write("\n")

print (gplot)
