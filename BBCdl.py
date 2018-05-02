#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import time
import urllib
import signal

urlbase = 'http://bbcsfx.acropolis.org.uk/assets/'
csvfile = 'BBCSoundEffects.csv'

def signal_handler(signal, frame):
    print 'KeyboardInterrupt'
    sys.exit(1)

def download(url, fname, i=None, total=None):
    download = ""

    if not os.path.isfile(fname):
        while not download == "end":
            if i == None or total == None:
                print "Downloading file " + url + " as " + fname
            else:
                print "Downloading file " + str(i) + "/" + str(total) + ": " + url + " as " + fname
            try:
                urllib.urlretrieve(url, fname)
                download = "end"
            except Exception as e:
                # The server is often micro-inaccessible
                print "Error, retrying: " + str(e)
                time.sleep(5)
                if os.path.isfile(fname):
                    os.remove(fname)
                download = "incomplete"

# Trap ^C
signal.signal(signal.SIGINT, signal_handler)

# Download CSV
download(urlbase + csvfile, csvfile)

num_lines = sum(1 for line in open(csvfile)) + 1

with open(csvfile, 'rb') as csvfd:
    reader = csv.DictReader(csvfd, delimiter=',', quotechar='"')
    i      = 1
    # Headers:
    # ['location', 'description', 'secs', 'category', 'CDNumber', 'CDName', 'tracknum']
    for row in reader:
        i        = i + 1
        ext      = "." + row['location'].split(".")[1]
        fullurl  = urlbase + row['location']
        filename = row['CDNumber'] + "_" + row['tracknum'] + " " + row['description']
        # To avoid dir characters in name
        ## Unix
        filename = filename.replace('/', '_')
        ## Windows
        filename = filename.replace('\\', '_')
        # ext4 limit
        filename = filename[0:250] + ext

        download(fullurl, filename, i, num_lines)
