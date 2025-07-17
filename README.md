# StraboGeMSTranslator
Converts Strabo JSON Databases to a GeMS compliant JSONs.
Developed at the New Mexico Burearu of Geology and Mineral Resources.

This project is designed to streamline the the process of making StraboField Datasets ready for GeMS compliant publication. The resulting files are JSONs with GeMS attributes derived from the StraboField user inputs. Files generated from these scripts can be imported into an Arc GeoDatabase using the Import JSON tool in ArcPro. Features within a StraboField Dataset are divided by feature class and assigned attributes consistent with the GeMS database standards. 

Note: this translation is unidirectional, meaning that if data is manipulated within the Arc GeoDatabase the changes will not be reflected in the StraboField Dataset. Designing a workflow that does not require repeated field edits is suggested. Suggested workflows include 1) maintaining different StraboField Datasets for each field excursion, and 2) using GeoDatabase data to build basemaps tiles for StraboField (tiles are uneditable).

Start by downloading a GeoJSON version of a dataset from the StraboSpot server (any project). Download the entire directory published here and run StraboGEMTraslatorGUI.py in a python environment (eg. spyder). 

Steps for Operation:

-Run StraboGEMTraslatorGUI.py

-A GUI should appear

-Add the StraboField Dataset as the input parameter

-Input any user information and dataset name

-Choose an export location

-Load the StraboField Dataset

On loading users are given options on how to sort and assign attributes to each feature. Consider each feature carefully. Any changes made to the attributes must be saved

-Save sorting and attribute preferences

-Start translation

On completion all files are written to the output directory. Any suspected errors can be viewed and saved in the error report. Note: features with errors are still included in the resulting JSONs, typically with blank/missing attribute fields. The user should evaluate the significance of each error. Unknown errors may also exist and the user should review all features before publication. 
