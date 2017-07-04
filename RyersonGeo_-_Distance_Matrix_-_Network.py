##RyersonGeo - Distance matrix - network=name

##Consumer_Centroid_Layer=vector
##Consumer_Centroid_Layer_ID_Field=field Consumer_Centroid_Layer

##Centre_Point_Layer=vector
##Centre_Point_Layer_ID_Field=field Centre_Point_Layer

##Network_Layer=vector

##Output_Layer=output file

# Script: RyersonGeo_-_Distance_Matrix_-_Network.py
# Author: Michael Morrish
# Date: December 18, 2016
#
# This script takes in three input shapefiles and two field specifications and
# produces a network distance matrix.

# Imports.
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *

# Get the layers.
lyrConsumer = processing.getObject(Consumer_Centroid_Layer)
lyrCentre = processing.getObject(Centre_Point_Layer)
lyrNetwork = processing.getObject(Network_Layer)

# Get the fields.
fldConsumerID_index = lyrConsumer.fieldNameIndex(Consumer_Centroid_Layer_ID_Field)
fldCentreID_index = lyrCentre.fieldNameIndex(Centre_Point_Layer_ID_Field)

# Setup the graph analysis.
director = QgsLineVectorLayerDirector(lyrNetwork, -1, '', '', '', 3)
properter = QgsDistanceArcProperter()
director.addProperter(properter)
crs = lyrConsumer.crs()
builder = QgsGraphBuilder(crs)

# Need to prepare output layer and add new fields.
# New fields are simply the ID of the Centre.
# Loop through each Centre to construct new field names.
lyrOutput = processing.getObject(Output_Layer)
provider = lyrOutput.dataProvider() 

# Optimize feature request for this loop.
request1 = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([Centre_Point_Layer_ID_Field], lyrCentre.fields() )

# The loop.
for centreFeature in lyrCentre.getFeatures(request1):
    
    # Capture value of fldCentreID_index (current ID).
    currentCentreID = centreFeature[fldCentreID_index]

    # Add and name the field. Double type for distances.   
    new_field_name = currentCentreID    
    provider.addAttributes([QgsField(new_field_name, QVariant.Double)])
    lyrOutput.updateFields()

# Set the output layer for editing.
lyrOutput.startEditing()

# Optimize feature request for outer nested loop.
request2 = QgsFeatureRequest().setSubsetOfAttributes([Consumer_Centroid_Layer_ID_Field], lyrConsumer.fields() )
   
# Loop through each Consumer feature.
for consumerFeature in lyrConsumer.getFeatures(request2):
    
    # Capture value of fldConsumerID_index (current ID).
    currentConsumerID = consumerFeature[fldConsumerID_index]
    
    # Loop through each Centre feature.
    for centreFeature in lyrCentre.getFeatures():
        
        # Setup the graph analysis.
        director = QgsLineVectorLayerDirector(lyrNetwork, -1, '', '', '', 3)
        properter = QgsDistanceArcProperter()
        director.addProperter(properter)
        crs = lyrConsumer.crs()
        builder = QgsGraphBuilder(crs)
        
        # Capture value of fldCentreID_index (current ID).
        currentCentreID = centreFeature[fldCentreID_index]
        
        # Get the path start point (Consumer point location).
        consumerGeom = consumerFeature.geometry()
        pStart = QgsPoint(consumerGeom.asPoint().x(),consumerGeom.asPoint().y())
        
        # Get the path end point (Centre point location).
        centreGeom = centreFeature.geometry()
        pStop = QgsPoint(centreGeom.asPoint().x(),centreGeom.asPoint().y())
        
        # Build the graph.
        tiedPoints = director.makeGraph(builder, [pStart, pStop])
        graph = builder.graph()

        # Attach the start and end points to the graph.
        tStart = tiedPoints[0]
        tStop = tiedPoints[1]

        idStart = graph.findVertex(tStart)
        idStop = graph.findVertex(tStop)

        # Solve the shortest path problem with dijkstra.
        (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)

        if tree[idStop] == -1:
            # If a path cannot be found, print error msg.
            print "Path not found"
        else:
            # If a path can be found, build array of points in path.
            p = []
            curPos = idStop
            while curPos != idStart:
                p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
                curPos = graph.arc(tree[curPos]).outVertex();

            p.append(tStart)

            # Create a new feature and put the shortest path polyline in it.
            # Then get the length of that line.
    
            ftShortestPath = QgsFeature()
            ftShortestPath.setGeometry(QgsGeometry.fromPolyline(p))
            shortestPathNetworkDistance = ftShortestPath.geometry().length()
            
            # Set the network distance value of the new Centre field for 
            # the current Consumer and Centre.
            lyrOutput.startEditing()
            current_distmatrix_field = currentCentreID
            distmatrix_field_index = lyrOutput.fieldNameIndex(current_distmatrix_field)
            lyrOutput.changeAttributeValue(consumerFeature.id(), distmatrix_field_index,shortestPathNetworkDistance)
            lyrOutput.commitChanges()
            
# Commit the changes to the layer.
lyrOutput.commitChanges()