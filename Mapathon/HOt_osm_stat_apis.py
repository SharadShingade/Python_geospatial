#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################


import json
import sys      #Require module sys for reading program options
from osgeo import ogr
import urllib2
import time
import os

#http://giscienceblog.uni-hd.de/2016/07/04/a-monitoring-tool-for-openstreetmap-mapathons-in-python/
#https://github.com/Hagellach37/osm_monitoring_tool/blob/master/run.py
'''
/api/v1/stats/project/{project_id}/activity # Get user actvity on a project
/api/v1/stats/project/{project_id}/contributions #Get all user contributions on a project
/api/v1/stats/project/{project_id}/user/{username} Get detailed stats about user
'''
 
req = urllib2.Request('https://tasks.hotosm.org/api/v1/stats/project/6404/activity')

resp = urllib2.urlopen(req)
content = resp.read()
mapathon_activity = json.loads(content)

for x in range(0,10):
    user = str(mapathon_activity['activity'][x]['actionBy'])
    task_id =str(mapathon_activity['activity'][x]['taskId']) 
    action_status = str(mapathon_activity['activity'][x]['actionText'])
    
    print user
    print task_id
    print action_status