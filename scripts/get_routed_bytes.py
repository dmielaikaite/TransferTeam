#!/usr/bin/env python
import sys
import os
import json
import urllib2

## Get the volume routed to a site given the CMS site name + Phedex queue (priority)
## This tools uses Phedex API routedblocks
## USAGE: python get_routed_bytes.py <CMS Site>

def formatSize(size):
    output = ''
    if size < 1E3:
        output += "%i B" % size
    elif size < 1E6:
        output += "%.3f kB" % (float(size)/1E3)
    elif size < 1E9:
        output += "%.3f MB" % (float(size)/1E6)
    elif size < 1E12:
        output += "%.3f GB" % (float(size)/1E9)
    elif size < 1E15:
        output += "%.3f TB" % (float(size)/1E12)
    elif size < 1E18:
        output += "%.3f PB" % (float(size)/1E15)
    return output

def get_routed_bytes(site):
    url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/routedblocks?to=' + site
    jstr = urllib2.urlopen(url).read()
    jstr = jstr.replace("\n", " ")
    result = json.loads(jstr)
    all_priorities = ["low", "normal", "high", "reserved"]
    bytes = 0
    for priority in all_priorities:
        get_priority(result,priority,bytes)

def get_priority(result,priority,bytes):
    for route in result['phedex']['route']:
        if (route['priority'] == priority):
            for block in route['block']:
                bytes += float(block['route_bytes'])
    final_record = priority + " "+ formatSize(bytes)
    print final_record

def init():
    get_routed_bytes(str(sys.argv[1]))

init()
