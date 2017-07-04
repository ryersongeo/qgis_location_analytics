##RyersonGeo - Distance matrix - euclidean=name

##Consumer_Centroid_Layer=vector
##Consumer_Centroid_Layer_ID_Field=field Consumer_Centroid_Layer

##Centre_Point_Layer=vector
##Centre_Point_Layer_ID_Field=field Centre_Point_Layer

##Output_Layer=output file

# Script: RyersonGeo_-_Distance_Matrix_-_Euclidean.py
# Author: Michael Morrish
# Date: December 18, 2016
#
# This script takes in two input shapefiles and two field specifications and
# produces a euclidean distance matrix.

# Imports.
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

# Get the layers.
lyrConsumer = processing.getObject(Consumer_Centroid_Layer)
lyrCentre = processing.getObject(Centre_Point_Layer)

# Get the fields.
fldConsumerID_index = lyrConsumer.fieldNameIndex(Consumer_Centroid_Layer_ID_Field)
fldCentreID_index = lyrCentre.fieldNameIndex(Centre_Point_Layer_ID_Field)

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
        
        # Capture value of fldCentreID_index (current ID).
        currentCentreID = centreFeature[fldCentreID_index]

        # Create a measurement object.
        mObject = QgsDistanceArea()
        
        # Measure the euclidean distance.
        eDistance = mObject.measureLine(consumerFeature.geometry().asPoint(), centreFeature.geometry().asPoint())

        # Set the euclidean distance value of the new Centre field for 
        # the current Consumer and Centre.
        current_distmatrix_field = currentCentreID
        distmatrix_field_index = lyrOutput.fieldNameIndex(current_distmatrix_field)
        lyrOutput.changeAttributeValue(consumerFeature.id(), distmatrix_field_index,eDistance)

# Commit the changes to the layer.
lyrOutput.commitChanges()