#!/usr/bin/python

# provide the name of a folder containing the required files as argv1

import sys
import os
from lxml import etree
from copy import deepcopy
import pprint

# check route name doesn't exist yet
# dict should have the form:
#	allRoutes = {'route-name1': [ [	{'lon': XXX, 'lat': XXX}, 
#					{'lon': XXX, 'lat': XXX}, ...], ... ],
#                     'route-name2': [ [{'lon': XXX, 'lat': XXX}, 
#					{'lon': XXX, 'lat': XXX}, ...], ... ],
# 			etc


TRANSXCHANGE_NAMESPACE = "http://www.transxchange.org.uk/"
TRANSXCHANGE = "{%s}" % TRANSXCHANGE_NAMESPACE
NSMAP = {"T" : TRANSXCHANGE_NAMESPACE}

routes = {}
# the data is provided in a zip containing 51 subfolders, so we need to walk subfolders
rootdir = sys.argv[1]
for dirName, subdirList, fileList in os.walk(rootdir):
	for filename in fileList:
		 
		route_name = filename.split("-")[1]
		if route_name not in routes:
			print filename
			
			routes[route_name] = []

			filePath = os.path.join(dirName, filename)
			tree = etree.parse(filePath)
			
			StopPointXP = etree.XPath("//T:StopPoint", namespaces=NSMAP)
			LonXP = etree.XPath("//T:Place//T:Location//T:Longitude", namespaces=NSMAP)
			LatXP = etree.XPath("//T:Place//T:Location//T:Latitude", namespaces=NSMAP)
			AtcoCodeXP = etree.XPath("//T:AtcoCode", namespaces=NSMAP)
			CommonNameXP = etree.XPath("//T:Descriptor//T:CommonName", namespaces=NSMAP)

			for elem in StopPointXP(tree):
				
				stopPoint = deepcopy(elem)
				lat = LatXP(stopPoint)[0].text
				lon = LonXP(stopPoint)[0].text
				#atcoCode = AtcoCodeXP(stopPoint)[0].text
				commonName = CommonNameXP(stopPoint)[0].text

				routes[route_name].append({	'lat': lat, 
								'lon': lon, 
								#'atcocode': atcoCode, 
								'name': commonName})
			#pp = pprint.PrettyPrinter(indent=4)
			#pp.pprint(routes)


		else: 
			print filename,  " exists already"


fo = open('sydneybuses.py', 'w')
fo.write('sydneybuses = '+  pprint.pformat(routes))
fo.close()


