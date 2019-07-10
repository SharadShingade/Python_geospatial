# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:48:45 2019

@author: Admin
"""

## https://github.com/taspinar/sidl/blob/master/notebooks/2_Detecting_road_and_roadtypes_in_sattelite_images.ipynb
# http://ataspinar.com/2017/12/04/using-convolutional-neural-networks-to-detect-features-in-sattelite-images/#ch1

#https://github.com/mahmoudmohsen213/airs
#https://geopython.github.io/OWSLib/
#http://ataspinar.com/about/


from owslib.wms import WebMapService
URL = "https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?request=GetCapabilities"
wms = WebMapService(URL, version='1.1.1')
 
OUTPUT_DIRECTORY = 'D:\Github\Python_geospatial\data\image_tiles/'

#OUTPUT_DIRECTORY = 'D:\Github\Python_geospatial\data\High_res_image_tiles/'
 
x_min = 90000
y_min = 427000
dx, dy = 200, 200
no_tiles_x = 100
no_tiles_y = 100
total_no_tiles = no_tiles_x * no_tiles_y
 
x_max = x_min + no_tiles_x * dx
y_max = y_min + no_tiles_y * dy
BOUNDING_BOX = [x_min, y_min, x_max, y_max]
 
for ii in range(0,no_tiles_x):
    print(ii)
    for jj in range(0,no_tiles_y):
        ll_x_ = x_min + ii*dx
        ll_y_ = y_min + jj*dy
        bbox = (ll_x_, ll_y_, ll_x_ + dx, ll_y_ + dy) 
        img = wms.getmap(layers=['Actueel_ortho25'], srs='EPSG:28992', bbox=bbox, size=(1256, 1256), format='image/jpeg', transparent=True)
        filename = "{}_{}_{}_{}.jpg".format(bbox[0], bbox[1], bbox[2], bbox[3])
        out = open(OUTPUT_DIRECTORY + filename, 'wb')
        out.write(img.read())
        out.close()
        
#img = wms.getmap(layers=['Actueel_ortho25'], srs='EPSG:4326', bbox=(-1.65729160235, 48.0405018704, 12.4317272654, 56.1105896442),size=(256, 256),format='image/jpeg',transparent=True)
#URL ="https://geowebservices.stanford.edu/geoserver/druid/wms?request=GetCapabilities"
#wms = WebMapService(URL, version='1.1.1')
#D:\Github\Python_geospatial\data\Wegvakken
        
        
def JSONencoder(obj):
    """JSON serializer for objects not serializable by default json code"""
 
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, bytes):
        return {'__class__': 'bytes',
                '__value__': list(obj)}
    raise TypeError ("Type %s not serializable" % type(obj))

import json
import shapefile
 
input_filename = 'D:\Github\Python_geospatial\data\Wegvakken\Wegvakken_Clip.shp'
output_filename = 'D:\Github\Python_geospatial\data\Wegvakken\Wegvakken.json'
 
reader = shapefile.Reader(input_filename)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 
 
#output_filename = './data/nwb_wegvakken/2017_09_wegvakken.json'
json_file = open(output_filename , "w")
json_file.write(json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2,default=JSONencoder) + "\n")
json_file.close()


####

from collections import defaultdict

dict_roadtype = {
    "G": 'Gemeente',
    "R": 'Rijk',
    "P": 'Provincie',
    "W": 'Waterschap',
    'T': 'Andere wegbeheerder',
    '' : 'leeg'
}
 
dict_roadtype_to_color = {
    "G": 'red',
    "R": 'blue',
    "P": 'green',
    "W": 'magenta',
    'T': 'yellow',
    '' : 'leeg'
}
 
FEATURES_KEY = 'features'
PROPERTIES_KEY = 'properties'
GEOMETRY_KEY = 'geometry'
COORDINATES_KEY = 'coordinates'
WEGSOORT_KEY = 'WEGBEHSRT'
 
MINIMUM_NO_POINTS_PER_TILE = 4
POINTS_PER_METER = 0.1
 
INPUT_FOLDER_TILES = 'D:\Github\Python_geospatial\data\image_tiles/'
 
 
filename_wegvakken = 'D:\Github\Python_geospatial\data\Wegvakken\Wegvakken.json'
dict_nwb_wegvakken = json.load(open(filename_wegvakken))[FEATURES_KEY]
d_tile_contents = defaultdict(list)
d_roadtype_tiles = defaultdict(set)

