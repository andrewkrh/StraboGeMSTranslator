# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 12:18:29 2024

@author: ahoxey
"""

import os
import csv

appcwd = os.getcwd()

# Build Global vairables
ErrorDict = dict()

LN_SB = []
LN_Gem_Sort = []
LN_Gem_Symbol =[]
LN_Gem_Type = []
PT_SB = []
PT_Gem_Sort = []
PT_Gem_Symbol = []
PT_Gem_Type = []


# GeMS configuration variables
LN_Sort_options = [ "ContactsAndFaults", "GeologicLines", "MapUnitLines", "CartagraphicLines"]
LN_Type_options = [### ContactsAndFaults
                  "contact","igneous contact", "intrusive contact", "metamorphic contact", 
                 "internal contact", "angular unconformity", 
                 "disconformity", "nonconformity", "paraconformity", 
                 "unconformity", "fault", "normal fault", "thrust fault", 
                 "reverse fault","right-lateral strike-slip fault", 
                 "left-lateral strike-slip fault", "right-lateral oblique-slip fault",
                 "left-lateral oblique-slip fault", "detachment fault", 
                 "low-angle normal fault", "fault scarp", "scarp", 
                 "elevation profile", "eolian", "escarpment", "geophysical fault", 
                 "gradational contact", "headscarp", "joint", "breccia", 
                 "miscellaneous map element", "map boundary",
                 #### GeologicLines
                 "anticline", "asymmetric anticline", "syncline", "asymmetric syncline", "breccia", 
                 "crest", "escarpment", "geophysical boundary", "geophysical survey", 
                 "headscarp", "landslide", "lineament", "lineation", "metamorphic facies", 
                 "monocline", "monocline, anticlinal bend", "monocline, synclinal bend", 
                 "overturned anticline", "overturned syncline", "scarp", "sedimentary facies", 
                 "shear zone",
                 ### MapUnitLines
                 "key bed", "dike", "clay bed", "coal bed", "N/A",               
                 #### CartagraphicLines
                 "analytical", "bedding line", "crest", "cross-section line", 
                 "feature label", "geophysical survey", "leader", "measured-section line", 
                 "miscellaneous map element", "scale change", "trench", "well"
                 ]


PT_Sort_options = [ "Stationns" , "GenericSamples", "OrientationPoints", "MapUnitPoints", "MapUnitPolyLabels"]
PT_Type_options = [ ### OrientationPoints
                   "anticline" , "bedding" , "crenulation lineation" , "cumulate foliation" , "dike inclination" ,
                   "eolian" , "fault" , "fault decoration" , "fault inclination" , "fault offset" , "fluvial" , 
                   "fold decoration" , "fold hinge" , "foliation" , "groundwater movement" , "intersection lineation" , 
                   "joint" , "landslide" , "lineation" , "local fault offset" , "mineral lineation" , "minor fault" , 
                   "minor fold" , "modern current" , "overturned bedding" , "paleocurrent" , "plunge" , 
                   "primary foliation" , "secondary foliation" , "slickenline" , "spring" , "stretching lineation" , 
                   "syncline" , "Toreva block"
                 ]

## FGDC Table
symbol_file=appcwd + "/resources/FGDC_Symbols_Table.csv"
with open(symbol_file, 'r') as file:
    reader = csv.DictReader(file)
    result = {}
    for row in reader:
        key = row['Symbol']  # Replace 'key_column' with the actual column name you want to use as the key
        result[key] = row
FGDC_Symbol_Table = result