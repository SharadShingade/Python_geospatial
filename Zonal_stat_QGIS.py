# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:43:04 2019

@author: Admin
"""

import processing

registry = QgsProject.instance()

Polygons = registry.mapLayersByName('Polygons_new')

iterator = Polygons[0].getFeatures()

feats_Polygons = [ feat for feat in iterator ]

Raster = registry.mapLayersByName('Raster')
rprovider = Raster[0].dataProvider()

xmin, ymin, xmax, ymax = Raster[0].extent().toRectF().getCoords()

extent = str(xmin)+ ',' + str(xmax)+ ',' +str(ymin)+ ',' +str(ymax) 

parameters = {"TYPE":2, 
              "EXTENT":extent, 
              "HSPACING":1000, 
              "VSPACING":1000,
              "HOVERLAY":0,
              "VOVERLAY":0, 
              "CRS":Raster[0].crs().authid(), 
              "OUTPUT":"/home/zeito/pyqgis_data/tmp_grid.shp"}

path = processing.run('qgis:creategrid', 
                         parameters)

grid = QgsVectorLayer(path['OUTPUT'],
                      'grid',
                      'ogr')

feats_grid = [ feat for feat in grid.getFeatures() ]

geom_pol = []
attr = []

for featg in feats_grid:
    for featp in feats_Polygons:
        if featg.geometry().intersects(featp.geometry()):
            geom = featg.geometry().intersection(featp.geometry())
            geom_pol.append(geom.asWkt())
            pt = geom.centroid().asPoint()
            value = rprovider.identify(pt,
                                       QgsRaster.IdentifyFormatValue).results()[1]
            attr.append([value, geom.area()])

epsg = Polygons[0].crs().postgisSrid()

uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer&field=value:double&field=area:double&field=w_value:double""&index=yes"

mem_layer = QgsVectorLayer(uri,
                           'polygon',
                           'memory')

prov = mem_layer.dataProvider()

feats = [ QgsFeature() for i in range(len(geom_pol)) ]

for i, feat in enumerate(feats):
    feat.setAttributes([i, attr[i][0], attr[i][1],(attr[i][0]*(attr[i][1]/1e6))])
    feat.setGeometry(QgsGeometry.fromWkt(geom_pol[i]))

prov.addFeatures(feats)

QgsProject.instance().addMapLayer(mem_layer)