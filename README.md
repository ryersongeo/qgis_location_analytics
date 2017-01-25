# qgis_location_analytics

_This QGIS toolset provides market research and location intelligence functions._

The location analytics tools for QGIS were developed by Mike Morrish for the [Department of Geography and Environmental Studies](http://www.ryerson.ca/geography/) at Ryerson University. The initial set of tools developed in December 2016 includes: 
- Euclidean distance calculation
- Network distance calculation
- Huff model

The development was supported by Profs. Claus Rinner and Stephen Swales through a 2016/17 RECODE grant entitled “Unlocking Data Analytics and Location Intelligence for the Non-Profit Sector”. RECODE funding from the J.W. McConnell Family Foundation is gratefully acknowledged. 

The grant proposal recognized that non-profit sector organizations increasingly have to operate like private sector enterprises in order to plan and manage program and service delivery and to secure sustained funding. Yet, non-profits do not have access to costly data analytics and business intelligence software that has become an essential component of large business operations. Through the grant, we aim to develop the prototype of a location analytics toolkit on the basis of a free and open-source Geographic Information System (GIS), QGIS. Our goal is to implement key analytics tools for geodemographic classification, service area delineation, and “sales” forecasts, translated to the needs of the non-profit sector. 

Among these tools, the Huff model is a spatial interaction model that is based on the principle of gravity. It combines the attractiveness of supply locations (destinations) with the distance that consumers have to travel, thereby representing competition between supply locations. The model assigns demand as the probability that consumers in a particular area (e.g. Census tract population) will use a particular supply location. Depending on the study at hand, these destinations could include shopping malls, health-care centres, or other service points. 

To generate the distance matrices between origins and destinations needed in the Huff model, a Euclidean distance script was created using QGIS’s standard distance calculation. In addition, a network distance script was implemented using QGIS’s network analysis library. 

Contact for development and technical questions: @michaelmorrish

Contact for research collaboration and applications: @crinner
