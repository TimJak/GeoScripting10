# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:11:31 2017

@author: Tim Jak & Koen Veenenbos
"""

#import the required packages
from osgeo import ogr, osr
import os
import folium
import subprocess

#Check if the driverName is available
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName(driverName)

if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print "%s driver IS available.\n" % driverName

#Create FileName and Layername
fn = "PointData.shp"
layername = "PointsForumAndBennekom"

#Create shapefile
ds = drv.CreateDataSource(fn)

#Set the correct coordinate system
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

#Create the layer
layer = ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)

#Create the points and give them the appropriate coordinates
Forum = ogr.Geometry(ogr.wkbPoint)
Bennekom = ogr.Geometry(ogr.wkbPoint)

Forum.SetPoint(0,5.663667,51.985418)
Bennekom.SetPoint(0,5.669566,52.005821)

#Create the feature layer
layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)

feature1.SetGeometry(Forum)
feature2.SetGeometry(Bennekom)

layer.CreateFeature(feature1)
layer.CreateFeature(feature2)

#Substract the KML information for Forum and Bennekom
Forumkml = Forum.ExportToKML()
Bennekomkml = Bennekom.ExportToKML()

#Paste this information in a text file and save it as .kml
string = "<Document><Placemark>" + Forumkml + "</Placemark><Placemark>" + Bennekomkml + "</Placemark></Document>"
fil = open("ForumBennekom.kml","w") 
fil.write(string)
fil.close()

ds.Destroy()

#Display the two points in a map
Bash = "ogr2ogr -f GeoJSON -t_srs crs:84 pointData.geojson PointData.shp"
ForumBennekomGeojson = subprocess.Popen(Bash, shell = True)

pointsGeo=os.path.join("pointData.geojson")
map_points = folium.Map(location=[52,5.7], tiles = 'Mapbox Bright', zoom_start = 6)
map_points.choropleth(geo_path=pointsGeo)
map_points.save('pointData.html')