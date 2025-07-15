# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:35:23 2024

@author: ahoxey

"""
######################################

## Translator function for StraboSpot2 data structure to GeMS Statemap standard.
## Reads exported JSON file from StraboSpot.org server.
## Function is initiated by GUI and could be called independently

########################################

import StraboWorkingConfig as SWG
import StraboGEMConfig as CONFIG


global CONFIG





# V1 = SWG.V1
# V2 = SWG.V2
# V3 =  SWG.V3 
# V4 = SWG.V4



def Translator(strabo_JSON_file, user_input_DSID, user_input_LSID, user_input_OSID, export_JSON_Dest, dataset_name):

    import json
    import StraboUtils as SU
    from pathlib import Path
       
    strabo_lines_list = list()
    strabo_points_list = list()
    errors = 0
    import_er = 0
    Line_er = 0
    Point_er = 0
    
    sp_count, import_er, strabo_lines_list, strabo_points_list = SU.ImportStrabo(strabo_JSON_file)
    #### Import Data

    

    #### Main function that performs translations; See StraboUtils.py for details          
    GM_ContactsAndFaults, GM_GeologicLines, GM_MapUnitLines, GM_CartographicLines, GM_nonTraceFeatures, Line_er = SU.StraboToGEMLines(strabo_lines_list, user_input_DSID, user_input_LSID) #### Passes List of disctionaries
    GM_Stations, GM_GenericSamples, GM_OrientationPoints, GM_MapUnitPoints, GM_MapUnitPolyLabels, Point_er = SU.StraboToGEMPoints(strabo_points_list, user_input_DSID, user_input_LSID, user_input_OSID)

    errors = errors + import_er + Line_er + Point_er
   
    # JSON_CF = json.dumps(GM_ContactsAndFaults, indent = 2)
    # with open('j_data_file.json', 'w') as outfile:
    #     outfile.write(JSON_CF)
    
    
    
    #### Export translated dictionaries to new JSON files
    base = Path(export_JSON_Dest)
    base.mkdir(exist_ok=True)
    
    #### check that these are Arc-readable JSON, boooo esri
    #### Consider adding DB Name to filenames (user input in GUI)
    #print(GM_ContactsAndFaults)
    jsonpath = base/(dataset_name + "_ContactsAndFaults.json")
    jsonpath.write_text(json.dumps(GM_ContactsAndFaults, indent=2))
    
    jsonpath = base/(dataset_name + "_GeologicLines.json")
    jsonpath.write_text(json.dumps(GM_GeologicLines, indent=2))
    
    jsonpath = base/(dataset_name + "_MapUnitLines.json")
    jsonpath.write_text(json.dumps(GM_MapUnitLines, indent=2))
    
    jsonpath = base/(dataset_name + "_CartographicLines.json")
    jsonpath.write_text(json.dumps(GM_CartographicLines, indent=2))
    
    jsonpath = base/(dataset_name + "_Stations.json")
    jsonpath.write_text(json.dumps(GM_Stations, indent=2))
    
    jsonpath = base/(dataset_name + "_GenericSamples.json")
    jsonpath.write_text(json.dumps(GM_GenericSamples, indent=2))
    
    jsonpath = base/(dataset_name + "_OrientationPoints.json")
    jsonpath.write_text(json.dumps(GM_OrientationPoints, indent=2))
    
    jsonpath = base/(dataset_name + "_MapUnitPoints.json")
    jsonpath.write_text(json.dumps(GM_MapUnitPoints, indent=2))
    
    jsonpath = base/(dataset_name + "_MapUnitPolyLabels.json")
    jsonpath.write_text(json.dumps(GM_MapUnitPolyLabels, indent=2))
    
    return errors, sp_count


# er, cnt = Translator(V1, V2, V3, V4)

# print(cnt, "StraboSpot(s) processed with ", er, " known errors")
