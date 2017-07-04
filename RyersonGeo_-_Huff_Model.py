##RyersonGeo - Huff model=name

##Consumer_Layer_with_Distance_Matrix=vector
##Consumer_Layer_ID_Field=field Consumer_Layer_with_Distance_Matrix
##Centre_Layer=vector
##Centre_Layer_ID_Field=field Centre_Layer
##Centre_Layer_Attractiveness_Field=field Centre_Layer
##Huff_Exponent_Value=selection 0.5; 1.0; 1.5; 2.0; 2.5; 3.0
##Output_Layer=output file

# Script: RyersonGEo - Huff Model
# Author: Michael Morrish
# Date: July 2, 2017
#
# This script takes in two input shapefiles, three field specifications, and
# one numeric value to produce Huff model probabilities.


# Imports.
from qgis.core import *
from PyQt4.QtCore import *

# Get the layers.
lyrConsumer = processing.getObject(Consumer_Layer_with_Distance_Matrix)
lyrCentre = processing.getObject(Centre_Layer)

# Get the fields.
fldConsumerID_index = lyrConsumer.fieldNameIndex(Consumer_Layer_ID_Field)
fldCentreID_index = lyrCentre.fieldNameIndex(Centre_Layer_ID_Field)
fldCentreAttract_index = lyrCentre.fieldNameIndex(Centre_Layer_Attractiveness_Field)

# Use dropdown list index to specify the Huff model exponent.
if Huff_Exponent_Value == 0:
    expHuff = 0.5
elif Huff_Exponent_Value == 1:
    expHuff = 1.0
elif Huff_Exponent_Value == 2:
    expHuff = 1.5
elif Huff_Exponent_Value == 3:
    expHuff = 2.0
elif Huff_Exponent_Value == 4:
    expHuff = 2.5
elif Huff_Exponent_Value == 5:
    expHuff = 3.0
    

# Need to prepare output layer and add new field.
# New field is "Hi" plus the ID of the Centre.
# Loop through each Centre to construct new field names.
lyrOutput = processing.getObject(Output_Layer)
provider = lyrOutput.dataProvider() 

for centreFeature in lyrCentre.getFeatures():
    
    # Capture value of fldCentreID_index (current ID).
    currentCentreID = centreFeature[fldCentreID_index]

    # Add and name the field.   
    new_field_name = 'Hi' + currentCentreID    
    provider.addAttributes([QgsField(new_field_name, QVariant.Double)])
    lyrOutput.updateFields()

# Set the output layer for editing.
lyrOutput.startEditing()

# Loop through each Consumer feature.
for consumerFeature in lyrConsumer.getFeatures():
    
    # Capture value of fldConsumerID_index (current ID).
    currentConsumerID = consumerFeature[fldConsumerID_index]
    
    # Create a total variable for the sumJ of Sj/dij values for use in the nested loop.
    sumJ_sjdivdij = 0.0
    
    # Huff Formula: [(sj/(dij)^b)/(SUMj(sj/(dij)^b))] for a given consumer i and centre j.
    # sumJ_sjdivdij is the denominator of this formula and is first loop below.
    # Exponent b is for friction of distance of the product or service.
    # Second loop below calculates numerator and completes Huff calc for a given ij.
    
    # Loop through each Centre feature to calculate a consumer's sumJ_sjdivdij.
    # This is the Huff formula denominator.
    for centreFeature in lyrCentre.getFeatures():
        
        # Capture value of fldCentreID_index (current ID).
        currentCentreID = centreFeature[fldCentreID_index]
        
        # Capture value of fldCentreAttract_index (current Centre Attractiveness).
        currentCentreAttract = centreFeature[fldCentreAttract_index]
        
        # Capture distance value for this Centre and this Consumer.
        # currentCentreID should match to field name in attrib table.
        currentDistance = consumerFeature[currentCentreID]
        
        # Calculate Centre Attractiveness / Distance^b >> (Sj/dij**b)
        
        # If statement to manage computing cost of exponent calculation.
        if expHuff == 1:
            sjdivdij = currentCentreAttract / currentDistance
        else:
            sjdivdij = currentCentreAttract / (currentDistance**expHuff)
        
        # Add new Sj/dij^b to sumJ_sjdivdij.
        sumJ_sjdivdij = sumJ_sjdivdij + sjdivdij
        
    # Loop through each Centre a second time to calculate Huff proportion.
    for centreFeature in lyrCentre.getFeatures():
        
        # Capture value of fldCentreID_index (current ID).
        currentCentreID = centreFeature[fldCentreID_index]
        
        # Capture value of fldCentreAttract_index (current Centre Attractiveness).
        currentCentreAttract = centreFeature[fldCentreAttract_index]
        
        # Capture distance value for this Centre and this Consumer.
        # currentCentreID should match to field name in attrib table.
        currentDistance = consumerFeature[currentCentreID]
        
        # Calculate Centre Attractiveness / Distance^b >> (Sj/dij**b)
        
        # If statement to manage computing cost of exponent calculation.
        if expHuff == 1:
            sjdivdij = currentCentreAttract / currentDistance
        else:
            sjdivdij = currentCentreAttract / (currentDistance**expHuff)
        
        # Complete the Huff formula calculation.
        calcHuffI = sjdivdij / sumJ_sjdivdij

        # Set the value of the new Hi field for the current Consumer and Centre.
        current_Huff_field = 'Hi' + currentCentreID
        Huff_field_index = lyrOutput.fieldNameIndex(current_Huff_field)
        lyrOutput.changeAttributeValue(consumerFeature.id(), Huff_field_index,calcHuffI)

# Commit the changes to the layer.
lyrOutput.commitChanges()