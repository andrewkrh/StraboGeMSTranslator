# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 16:47:07 2024

@author: ahoxey
"""
#### Series of nested functions that sort and assign GeMS attributes to features
#### created in StraboSpot2


##### Initial feature class sorting funtions
import StraboLineAttributeTranslators as LT
import StraboPointAttributeTranslators as PT
import StraboGEMConfig as CONFIG
#import StraboUserCustomAttributes as Cust

global CONFIG

############ 
### Initiating Functions

def ImportStrabo(strabo_JSON_file):
    import json
    
    strabo_points = []
    strabo_lines = []
    er = 0
    
    with open(strabo_JSON_file) as f:
        strabo_import = json.load(f) ### Nested Python Dictionary
    strabo_spots_list = strabo_import.get("features")

    count = len(strabo_spots_list)

    #### Sorts Strabo data by object type (line or point)
    for i in range(0, len(strabo_spots_list)):
        spot_type = strabo_spots_list[i].get("geometry").get("type")
        if spot_type == "Point":
            strabo_points.append(strabo_spots_list[i])
  
        elif spot_type == "LineString":
            if "trace" not in strabo_spots_list[i].get("properties"):
                er += 1 
                er_count = "Import Error " + str(er)
                CONFIG.ErrorDict[er_count] = strabo_spots_list[i].get("properties").get("name")
            else:
                strabo_lines.append(strabo_spots_list[i])
        else: 
            er += 1 
            er_count = "Import Error " + str(er)
            CONFIG.ErrorDict[er_count] = strabo_spots_list[i].get("properties").get("name")
    ## Do Nothing comand?
    return count, er, strabo_lines, strabo_points

def StraboToGEMLines(sb_lines, userID, locID):
    #### Sorts and executes line translations
    #### Takes in Lists of Dictionaries that describe each Strabo Line
    #### Returns a series of lists that are sorted by GeMS feature class
    #### Each list contains dictionaries that describe each line feature with attributes modified to reflect GeMS style
    
    gem_temp_dict = dict()
    TraceFeatures = list()
    nonTraceFeatures = list()
    gem_ContactsFaults = list()
    gem_GeologicLines = list()
    gem_MapUnitLines = list()
    gem_CartographicLines = list()
    ln_errors = 0
   
    #### Sort out non-trace feature line types; Ideally results in flagged line on ArcImport
    for x in range(0, len(sb_lines)):  ### Sort by trace non-trace
          strabo_properties = sb_lines[x].get("properties")
          if "trace" in strabo_properties.keys(): ##and "trace_feature" == True :
               TraceFeatures.append(sb_lines[x]) 
          else:
               nonTraceFeatures.append(sb_lines[x])
    
                
    #### Perform translations of all trace feature line types       
    for y in range(0, len(TraceFeatures)):
            gem_temp_dict = {}        
            SB_Trace_Str = ""
            SB_Trace_Str = getSBLineTraceString(TraceFeatures[y].get("properties"))
            sb_spot_name = TraceFeatures[y].get("properties").get("name")
            
            sort = ""  
            index = CONFIG.LN_SB.index(SB_Trace_Str)
            sort = CONFIG.LN_Gem_Sort[index]
            
            ### Make a new dictionary with GeMS attributes
            if sort == "ContactsAndFaults": 
                    gem_temp_dict["type"] = "Feature"    
                    gem_temp_dict["geometry"] = TraceFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToContactsAndFaults(SB_Trace_Str)
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"]  = str(sb_spot_name) + " " +  "Notes: " + TraceFeatures[y].get("properties").get("trace").get("trace_notes", "")
                        
                    
                    gem_ContactsFaults.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
            
            elif sort == "GeologicLines":
                    gem_temp_dict["type"] = "Feature"    
                    gem_temp_dict["geometry"] = TraceFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToGeologicLines(SB_Trace_Str)
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"]  = str(sb_spot_name) + " " + "Notes: " + TraceFeatures[y].get("properties").get("trace").get("trace_notes", "")
                    
                    gem_GeologicLines.append(gem_temp_dict)  #### Sending a sb_line.dict(), returns dict(), adds to GeolLine list
            
            elif sort == "MapUnitLines":
                    if "tags" in TraceFeatures[y].get("properties").keys():
                        line_unit_tag = TraceFeatures[y].get("properties").get("tags")
                        if len(line_unit_tag) > 1:
                            ln_errors += 1 
                            er_count = "Line Error " + str(ln_errors) + " multiple map units"
                            CONFIG.ErrorDict[er_count] = sb_spot_name
                        else: None
                    else:
                        ln_errors += 1 
                        er_count = "Line Error " + str(ln_errors) + " no map unit"
                        CONFIG.ErrorDict[er_count] = sb_spot_name
            
                    gem_temp_dict["type"] = "Feature"
                    gem_temp_dict["geometry"] = TraceFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToMapUnitLines(SB_Trace_Str, TraceFeatures[y].get("properties"))
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"]  =  str(sb_spot_name) + " " + "Notes: " + TraceFeatures[y].get("properties").get("trace").get("trace_notes", "")
                
                    gem_MapUnitLines.append(gem_temp_dict)  #### Sending a sb_line.dict(), returns dict(), adds to MUL list  
                    
            elif sort == "CartagraphicLines":
                    gem_temp_dict["type"] = "Feature"
                    gem_temp_dict["geometry"] = TraceFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToCartographicLines(SB_Trace_Str, TraceFeatures[y].get("properties"))
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"]  =  str(sb_spot_name) + " " + "Notes: " + TraceFeatures[y].get("properties").get("trace").get("trace_notes", "")
                        
                    gem_CartographicLines.append(gem_temp_dict)  #### Sending a sb_line.dict(), returns dict(), adds to CartLine list  
            else: pass
     
    GM_ContactsAndFaults = {"type": "FeatureCollection",
                            "features": gem_ContactsFaults}
    GM_GeologicLines = {"type": "FeatureCollection",
                            "features": gem_GeologicLines}
    GM_MapUnitLines = {"type": "FeatureCollection",
                            "features": gem_MapUnitLines}
    GM_CartographicLines = {"type": "FeatureCollection",
                            "features": gem_CartographicLines}
    GM_nonTraceFeatures = {"type": "FeatureCollection",
                            "features": nonTraceFeatures}
                                                  
    return GM_ContactsAndFaults, GM_GeologicLines, GM_MapUnitLines, GM_CartographicLines, GM_nonTraceFeatures, ln_errors

def StraboToGEMPoints(sb_points, userID, locID, orienID):
    #### Sorts and executes point translations
    #### Takes in Lists of dictionaries that describe each Strabo point data
    #### Returns a series of lists that are sorted by GEM feature class
    #### Each list contains dictionaries that describe each point with attributes modified to reflect GEM style

    #### Consctruction of Point data results in duplicated points where strabo points are "un-nested"
    #### For example: a spot that houses orientation data, a unit tag, and an image will result in
    #### multiple features (OrientationPoint(s), MapPolyLabel, and a Station)
    #### Each time an "daughter" point is produced the spot name is appended (spot_name_d1, spot_name_d2, etc.)

    gem_temp_dict = dict()
    PointFeatures = list()
    
    gem_Stations = list()
    gem_GenericSamples = list()
    gem_OrientationPoints = list()
    gem_MapUnitPoints = list()
    gem_MapUnitPolyLabels = list()
    pt_errors = 0
    #gem_GeochronPoints = list() #### NOT INCLUDED (NOT FIELD DATA)
    #gem_GenericPoints = list() (well data)
    
    #### Sort out non-data points ------ probabaly won't need this as all points have some form of data in them
    # for x in range(0, len(sb_points)):  ### Sort by trace non-trace
    #        strabo_properties = sb_points[x].get("properties")
    #        if "po_feature_type" in strabo_properties.keys(): ##and "po_feature" == True :
    #            PointFeatures.append(sb_points[x]) 
    #        else:
    #             nonPointFeatures.append(sb_points[x])
    
    PointFeatures = sb_points
                
    #### Perform translations of all point feature types       
    for y in range(0, len(sb_points)):
            gem_temp_dict = {}        
            
            
            # sort = []  #### 1 = Stationns; 2 = GenericSamples; 3 = OrientationPoints; 4 = MapUnitPoints; 5 = MapUnitPolyLabels;
            # # if CONFIG.Cust_Setting == 2:
            # #     sort = Cust.SortPointFeature_custom(PointFeatures[y].get("properties"))
            # # else:
            # sort = SortPointFeatureClass(PointFeatures[y].get("properties"))
                
                
            sort = []  #### 1 = Stations; 2 = GenericSamples; 3 = OrientationPoints; 4 = MapUnitPoints, 5 = MapPolyLabels, 6 = unsorted;           
            sort = SortPointFeatureClass(PointFeatures[y].get("properties"))
            
            sb_spot_name = PointFeatures[y].get("properties").get("name")
            spot_daughter_count = 0  
            
            ### Make a new dictionary with GeMS attributes
            if 1 in sort: #### Stations
                    if "tags" in PointFeatures[y].get("properties").keys():
                        point_unit_tag = PointFeatures[y].get("properties").get("tags")
                        if len(point_unit_tag) > 1:
                            pt_errors += 1 
                            er_count = "Point Error " + str(pt_errors) + " multiple map units"
                            CONFIG.ErrorDict[er_count] = sb_spot_name
                        else: None

                    gem_temp_dict = {}
                    gem_temp_dict["type"] = "Feature"
                    gem_temp_dict["geometry"] = PointFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToStations(PointFeatures[y].get("properties"))
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"] =  str(sb_spot_name) + "_"+ str(spot_daughter_count) + " " + gem_temp_dict["properties"]["Notes"]
                            
                    
                    gem_Stations.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
                    spot_daughter_count += 1
                    
            if 2 in sort: #### GenericSamples ##### NEEDS SIGNIFICANT MODIFICATION  ########
                    #Determine how many samples are in each spot                    
                    s_count_er=0
                    sb_sample_list =PointFeatures[y].get("properties").get("samples")
                    ## Returns a list of dictionaries with sample information (each sample results in it's own dictionary)
                    s_count_er = len(sb_sample_list)
                    
                    s = 0
                    while s < s_count_er:
                        gem_temp_dict = {}
                        gem_temp_dict["type"] = "Feature"
                        gem_temp_dict["geometry"] = PointFeatures[y].get("geometry")
                        gem_temp_dict["properties"] = StraboToSamples(sb_sample_list[s], PointFeatures[y].get("properties"))
                        gem_temp_dict["properties"]["DataSourceID"]=userID
                        gem_temp_dict["properties"]["LocationSourceID"]=locID
                        gem_temp_dict["properties"]["Notes"] =  str(sb_spot_name) + "_"+ str(spot_daughter_count) + " " + gem_temp_dict["properties"]["Notes"]
    
                        gem_GenericSamples.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
                        spot_daughter_count += 1
                        s += 1

            if 3 in sort: #### OrientationPoints
                    #Determine how many orientation measurements are in each spot                    
                    count_er=0
                    # OrKeys =PointFeatures[y].get("properties").keys()
                    # for K in OrKeys:
                    #   j = K.find("unix_timestamp")
                    #   if(j!=-1):
                    #     count_er+=1
                    
                    sb_orientation_list, count_er = OrientationParser(PointFeatures[y].get("properties").get("orientation_data"))
                                        
                    i = 0
                    while i < count_er:
                        orientation_str = ""
                        orientation_str = getSBOrientationString(sb_orientation_list[i])
                        
                        gem_temp_dict = {}
                        gem_temp_dict["type"] = "Feature"
                        gem_temp_dict["geometry"] = PointFeatures[y].get("geometry")
                        gem_temp_dict["properties"] = StraboToOrientations(orientation_str, sb_orientation_list[i], PointFeatures[y].get("properties"))
                        gem_temp_dict["properties"]["DataSourceID"]=userID
                        gem_temp_dict["properties"]["LocationSourceID"]=locID
                        gem_temp_dict["properties"]["OrientationSourceID"]=orienID
                        gem_temp_dict["properties"]["StationsID"]=str(sb_spot_name) + "_"+ str(spot_daughter_count)
                        gem_temp_dict["properties"]["Notes"] =  str(sb_spot_name) + "_"+ str(spot_daughter_count) + " " + gem_temp_dict["properties"]["Notes"]        

                        gem_OrientationPoints.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
                        spot_daughter_count += 1
                        i += 1
        
            if 4 in sort: #### MapUnitPoints
                    gem_temp_dict = {}
                    gem_temp_dict["type"] = "Feature"
                    gem_temp_dict["geometry"] = PointFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToMapUnitPoints(PointFeatures[y].get("properties"))
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"] =  str(sb_spot_name) + "_"+ str(spot_daughter_count) + " " + gem_temp_dict["properties"]["Notes"]       
    
                    gem_MapUnitPoints.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
                    spot_daughter_count += 1

            if 5 in sort: #### MapUnitPolyLabels
                    if "tags" in PointFeatures[y].get("properties").keys():
                            point_unit_tag = PointFeatures[y].get("properties").get("tags")
                            if len(point_unit_tag) > 1:
                                pt_errors += 1 
                                er_count = "Point Error " + str(pt_errors) + " multiple map units"
                                CONFIG.ErrorDict[er_count] = sb_spot_name
                            else: None
                                
                    gem_temp_dict = {}
                    gem_temp_dict["type"] = "Feature"
                    gem_temp_dict["geometry"] = PointFeatures[y].get("geometry")
                    gem_temp_dict["properties"] = StraboToMapUnitPolyLabels(PointFeatures[y].get("properties"))
                    gem_temp_dict["properties"]["DataSourceID"]=userID
                    gem_temp_dict["properties"]["LocationSourceID"]=locID
                    gem_temp_dict["properties"]["Notes"] =  str(sb_spot_name) + "_"+ str(spot_daughter_count)      

                    gem_MapUnitPolyLabels.append(gem_temp_dict) #### Sending a sb_line.dict(), returns dict(), adds to C&F list
                    spot_daughter_count += 1

            if 6 in sort:
                    pass
                ### return an unprocessed point
                    
                 
    GM_Stations = {"type": "FeatureCollection", "features": gem_Stations}
    GM_GenericSamples = {"type": "FeatureCollection", "features": gem_GenericSamples}
    GM_OrientationPoints = {"type": "FeatureCollection", "features": gem_OrientationPoints}
    GM_MapUnitPoints = {"type": "FeatureCollection", "features": gem_MapUnitPoints}
    GM_MapUnitPolyLabels = {"type": "FeatureCollection", "features": gem_MapUnitPolyLabels}
                    
    return   GM_Stations, GM_GenericSamples, GM_OrientationPoints, GM_MapUnitPoints, GM_MapUnitPolyLabels, pt_errors

def SortLineFeatureClass(sb_trace_str):
    #### Decision tree that sorts through strabo line characterizations
    #### 1 = ContactsAndFaults; 2 = GeologicLines; 3 = MapUnitLines; 4 = CartographicLines; 5 = Default Unsorted
    tempSort = ""
    
    if "contact" or "geologic_struc" in sb_trace_str:
        tempSort = "ContactsAndFaults"
        if "dike" in sb_trace_str:
            tempSort = "MapUnitLines"
        elif "sill" in sb_trace_str:
            tempSort = "MapUnitLines"
        elif "marker_layer" in sb_trace_str:
            tempSort = "MapUnitLines"
        
        elif "fold_axial_tra" in sb_trace_str:
            tempSort = "GeologicLines"
                
    elif "geomorphic_fea" in sb_trace_str:    
        tempSort = "GeologicLines"     
            
    elif "anthro" in sb_trace_str:    
        tempSort = "DefaultUnsorted"
            
    elif "scale_bar" in sb_trace_str:    
        tempSort = "DefaultUnsorted"
    
    elif "bedding" in sb_trace_str:    
        tempSort = "DefaultUnsorted"
    
    elif "geologic_cross" in sb_trace_str:    
        tempSort = "CartographicLines"
    
    elif "geophysical_cross" in sb_trace_str:    
        tempSort = "CartographicLines"

    elif "other_feature" in sb_trace_str:    
        tempSort = "DefaultUnsorted"
        
    else: tempSort = "DefaultUnsorted"

    return tempSort

def SortPointFeatureClass(Features):    #### incomplete; needs language update for sample information
    #### Decision tree that sorts through strabo point data characterizations
    #### Takes Feature.Properties dict
    #### 1 = Stations; 2 = GenericSamples; 3 = OrientationPoints; 4 = MapUnitPoints, 5 = MapPolyLabels, 6 = unsorted;
    tempSort = []
    
    if "images" in Features.keys():
        if not Features.get("images"):  #### Check that the container is not empty
            pass
        else:   
            #Spot images
            tempSort.extend([1])
    if "notes" in Features.keys():
        if not Features.get("notes"):  #### Check that the container is not empty
            pass
        else:   
            #Spot likely only includes notes
            tempSort.extend([1])
        
    if "samples" in Features.keys(): 
        if not Features.get("samples"):  #### Check that the container is not empty
            pass
        else:   
            #Spot includes a sample
            #print('I found a sample:', Features.get("name") )
            tempSort.extend([2])
        
    if "orientation_data" in Features.keys(): 
        if not Features.get("orientation_data"):  #### Check that the container is not empty
            pass
        else:        
            #Spot includes an orientation measurement
            tempSort.extend([3])
      
    tempvar = 0
    if "tags" in Features.keys(): 
        if not Features.get("tags"):  #### Check that the container is not empty
            pass
        else:
            sb_tags = Features.get("tags")
            for n in range(0, len(sb_tags)):
                if sb_tags[n].get("type") == "concept":
                    tempSort.extend([1])
                else:
                    tempvar = 5
            #Spot includes a unit tag
            tempSort.extend([tempvar])
       
       
       
    return tempSort
    

#############################
#### Parsing and Attribute building functions unique to each feature class

## line data
def getSBLineTraceString(sb_line_prop):
    ### takes Strabo attributes and consolidates them to a string variable
    
    trace_dict = sb_line_prop.get("trace")
    trace_type = ""
    
    for v in trace_dict:
        if v != "trace_feature" and v != "modified_timestamp":
            trace_type = trace_type + trace_dict[v] + " "
        else: None

    return trace_type

def StraboToContactsAndFaults(sb_line_str):
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single line feature Properties Dictionary (nested) with Strabo attributes
    ## All lines sent to function must be ContactsAndFaults
    
    ### make same size as StraboToCF?  
    gem_CF = dict()
    gem_CF = {
        "Type": "",
        "Label" : "",
        "Symbol" : "",
        "IsConcealed" : "",
        "IdentityConfidence" : "",
        "ExistenceConfidence" : "",
        "LocationConfidenceMeters" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
    
    
    index = CONFIG.LN_SB.index(sb_line_str)
    gem_CF["Symbol"]  = CONFIG.LN_Gem_Symbol[index]  
    gem_CF["Type"] = CONFIG.LN_Gem_Type[index]

    gem_CF["IdentityConfidence"] = LT.getIdentity(sb_line_str, gem_CF["Symbol"])      
    gem_CF["ExistenceConfidence"] = LT.getExistence(sb_line_str, gem_CF["Symbol"])
    gem_CF["LocationConfidenceMeters"] = LT.getLocation(sb_line_str, gem_CF["Symbol"])
    gem_CF["IsConcealed"] = LT.getConcealed(sb_line_str, gem_CF["Symbol"])
    
    return gem_CF

def StraboToGeologicLines(sb_line_str):
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single line feature dictionary with Strabo attributes
    ## All lines sent to function must be GeologicLines
    
    ### make same size as StraboToCF?  
    gem_GL = dict()
    gem_GL = {
        "Type" : "",
        "Label" : "",
        "Symbol" : "",
        "IsConcealed" : "",
        "IdentityConfidence" : "",
        "ExistenceConfidence" : "",
        "LocationConfidenceMeters" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
        
    index = CONFIG.LN_SB.index(sb_line_str)
    gem_GL["Symbol"]  = CONFIG.LN_Gem_Symbol[index]  
    gem_GL["Type"] = CONFIG.LN_Gem_Type[index]
     
    gem_GL["IdentityConfidence"] = LT.getIdentity(sb_line_str, gem_GL["Symbol"])   
    gem_GL["ExistenceConfidence"] = LT.getExistence(sb_line_str, gem_GL["Symbol"])
    gem_GL["LocationConfidenceMeters"] = LT.getLocation(sb_line_str, gem_GL["Symbol"])
    gem_GL["IsConcealed"] = LT.getConcealed(sb_line_str, gem_GL["Symbol"])
        
    return gem_GL

def StraboToMapUnitLines(sb_line_str, sb_line_dict):
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single line feature dictionary with Strabo attributes
    ## All lines sent to function must be MapUnitLines
    
    ### make same size as StraboToCF?  
    gem_MUL = dict()
    gem_MUL = {
        #"Type" : "",
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "",
        "IsConcealed" : "",
        "IdentityConfidence" : "",
        "ExistenceConfidence" : "",
        "LocationConfidenceMeters" : "",
        "PlotAtScale" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
    
        
    if "tags" in sb_line_dict.keys():
        sb_unit_tag, _ = getUnitTag(sb_line_dict)
        if not sb_unit_tag:  #### Check that the container is not empty (tag is associated with concept)
            pass
        else:
            gem_MUL["MapUnit"] = sb_unit_tag["unit_label_abbreviation"]
            gem_MUL["Label"] = PT.getUnitLabel(sb_unit_tag) ### use FGDC font
    
    else: 
        gem_MUL["MapUnit"] = "unassigned" 
        gem_MUL["Label"] = ""  ### use FGDC font""

        
    index = CONFIG.LN_SB.index(sb_line_str)
    gem_MUL["Symbol"]  = CONFIG.LN_Gem_Symbol[index]  
    #gem_MUL["Type"] = CONFIG.LN_Gem_Type[index]
    
    gem_MUL["IdentityConfidence"] = LT.getIdentity(sb_line_dict, gem_MUL["Symbol"])   
    gem_MUL["ExistenceConfidence"] = LT.getExistence(sb_line_dict, gem_MUL["Symbol"])
    gem_MUL["LocationConfidenceMeters"] = LT.getLocation(sb_line_dict, gem_MUL["Symbol"])
    gem_MUL["IsConcealed"] = LT.getConcealed(sb_line_dict, gem_MUL["Symbol"])

    
    #gem_MUL.pop("Type", None)
    
    return gem_MUL

def StraboToCartographicLines(sb_line_str, sb_line_dict):
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single line feature dictionary with Strabo attributes
    ## All lines sent to function must be CartographicLines
    
    ### make same size as StraboToCF?  
    gem_CL = dict()
    gem_CL = {
        "Type" : "",
        "Label" : "",
        "Symbol" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
        
    index = CONFIG.LN_SB.index(sb_line_str)
    gem_CL["Symbol"]  = CONFIG.LN_Gem_Symbol[index]  
    gem_CL["Type"] = CONFIG.LN_Gem_Type[index] 
    
    gem_CL["IdentityConfidence"] = LT.getIdentity(sb_line_dict, gem_CL["Symbol"])   
    
    return gem_CL

## point data  
def getSBOrientationString(sb_orientation_dict):
    ### takes Strabo measurement dict and returns a string description
    
    or_type = ""
    
    for v in sb_orientation_dict:
        if v != "id" and v != "strike" and v != "dip" and v != "trend" and v != "plunge" and v != "unix_timestamp" and v != "quality" and v != "modified_timestamp":
            or_type = or_type + sb_orientation_dict[v] + " "
        else: None
        
    return or_type

def OrientationParser(sb_orientation_dict): #### Incomplete
    ### Takes in Strabo Spot that houses multiple orientation measurements and parses them to multiple points
    ### 
    #### Likely need to be modified to address "associated orientations" P+L combinations
    count = 0
    orientation_list = []
    associated_list = []
    
    for m in range(0, len(sb_orientation_dict)):
        if "associated_orientation" in sb_orientation_dict[m].keys():
            associated_list = sb_orientation_dict[m].get("associated_orientation")
            for l in range(0, len(associated_list)):
                orientation_list.append(associated_list[l])
                count += 1
            sb_orientation_dict[m].pop("associated_orientation", None)
            orientation_list.append(sb_orientation_dict[m])
            count += 1
        else: None
        orientation_list.append(sb_orientation_dict[m])
        count += 1
            
    
    
    
    
    # UsingKeys = ([k for k in OrKeys if 'unix' in k]) #Makes list of "po_[count]_unix_timestamp"
    # UsingKeys = [l[:-14] for l in UsingKeys] #Makes list of "po_[count]"
    
    # if any("po" or "lo" in string for string in UsingKeys):
    #     for n in range(0, len(UsingKeys)): #build search keys "po_[count] + attribute"
    #         search_key1 = UsingKeys[n] + "feature_type"
    #         search_key2 = UsingKeys[n] + "facing"
    #         search_key3 = UsingKeys[n] + "facing_defined_by"
    #         search_key4 = UsingKeys[n] + "strike"
    #         search_key5 = UsingKeys[n] + "dip"
    #         search_key6 = UsingKeys[n] + "unix_timestamp"
    #         search_key7 = UsingKeys[n] + "quality"
    #         search_key8 = UsingKeys[n] + "feature_notes"
        
    #         search_key40 = UsingKeys[n] + "trend"
    #         search_key50 = UsingKeys[n] + "plunge"

                           

    #         orientation_dict = {}
    #         orientation_dict = {NewKey: {"feature_type": sb_point_dict.get(search_key1),
    #                                      "facing": sb_point_dict.get(search_key2, "NA"),
    #                                      "facing_defined_by": sb_point_dict.get(search_key3, "NA"),
    #                                      "strike": sb_point_dict.get(search_key4),
    #                                      "dip": sb_point_dict.get(search_key5),
    #                                      "trend": sb_point_dict.get(search_key40),
    #                                      "plunge": sb_point_dict.get(search_key50),
    #                                      "unix_timestamp": sb_point_dict.get(search_key6),
    #                                      "quality": sb_point_dict.get(search_key7, 5),
    #                                      "notes": sb_point_dict.get(search_key8, "")}
    #                             }
        
    #         orientation_list.append(orientation_dict)
    # else:
    #     None
    
    return orientation_list, count

def StraboToStations(sb_point_dict): ##### Incomplete
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single point feature dictionary with Strabo attributes
    sb_images = [] 
    
    gem_St = dict()
    gem_St = {
        "FieldID" : "",
        "ObservedMapUnit" : "", ##### What does this mean?
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "",
        "LocationConfidenceMeters" : "",
        "PlotAtScale" : "",
        "LocationMethod" : "",
        "GPSX" : "",
        "GPSY" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
    
    gem_St["FieldID"] = sb_point_dict["name"]
    
    if "tags" in sb_point_dict.keys():
        sb_unit_tag, _ = getUnitTag(sb_point_dict)
        if not sb_unit_tag:  #### Check that the container is not empty (tag is associated with concept)
            pass
        else:
            gem_St["MapUnit"] = sb_unit_tag["unit_label_abbreviation"]  
            gem_St["Label"] = PT.getUnitLabel(sb_unit_tag) ### use FGDC font
            gem_St["Symbol"] = sb_unit_tag["unit_label_abbreviation"]   ### consider subdivision for subscripts
    
    else: pass
    
    gem_St["Notes"] = "Notes: " + sb_point_dict.get("notes", "") + " Images: " 
    sb_images = sb_point_dict.get("images", "")
    for x in range(0, len(sb_images)):
        gem_St["Notes"] = gem_St["Notes"] + sb_images[x].get("self", "") + " "
    
        
    return gem_St
     
def StraboToSamples(sb_sample_dict, sb_point_dict): #### Incomplete
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single sample dictionary with Strabo attributes
    ## Add function to incorporate "inplaceness", etc.
     
    gem_Sam = dict()
    gem_Sam = {
        "Type" : "",
        "FieldSampleID" : "",
        "AlternateSampleID" : "",
        "ObservedMapUnit" : "",
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "31.21",
        "LocationConfidenceMeters" : "",
        "PlotAtScale" : "",
        "MaterialAnalyzed" : "",
        "StationsID" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "AnalysisSourceID" : "",
        "Notes" : ""}
    
    gem_Sam["Type"] = PT.getSamType(sb_sample_dict) ### passing a dict()
    gem_Sam["FieldSampleID"] = sb_sample_dict["sample_id_name"]
    gem_Sam["StationID"] = sb_point_dict["name"]
    gem_Sam["Notes"] = "Notes: " + sb_sample_dict.get("sample_description", "") + " / " + sb_sample_dict.get("sample_notes", "")
    ### Consider ways to add "inplaceness" and orientations
    
    if "tags" in sb_point_dict.keys():
        sb_unit_tag, _ = getUnitTag(sb_point_dict)
        if not sb_unit_tag:  #### Check that the container is not empty (tag is associated with concept)
            pass
        else:
            gem_Sam["MapUnit"] = sb_unit_tag["unit_label_abbreviation"]  
            gem_Sam["Label"] = PT.getUnitLabel(sb_unit_tag) ### use FGDC font   
    else: pass
    
    return gem_Sam
    
def StraboToOrientations(sb_orientation_str, sb_orientation_dict, sb_point_dict): #### incomplete; Confidence
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single point feature dictionary with Strabo attributes
     
    gem_Or = dict()
    gem_Or = {
        "Type" : "",
        "Azimuth" : "",
        "Inclination" : "",
        "ObservedMapUnit" : "",
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "",
        "LocationConfidenceMeters" : "",
        "OrientationConfidenceDegrees" : "",
        "PlotAtScale" : "",
        "StationsID" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "OrientationSourceID" : "",
        "Notes" : ""}
    
    index = CONFIG.PT_SB.index(sb_orientation_str)
    gem_Or["Symbol"]  = CONFIG.PT_Gem_Symbol[index]  
    gem_Or["Type"] = CONFIG.PT_Gem_Type[index]
    
    
    if "strike" in sb_orientation_dict:
        gem_Or["Azimuth"] = (sb_orientation_dict["strike"] + 90) % 360
    else: 

        gem_Or["Azimuth"] = sb_orientation_dict["trend"]
    
    if "dip" in sb_orientation_dict:
        gem_Or["Inclination"] = sb_orientation_dict["dip"]
    else: 
        gem_Or["Inclination"] = sb_orientation_dict["plunge"]

    
    if "tags" in sb_point_dict.keys():
        sb_unit_tag, _ = getUnitTag(sb_point_dict)
        if not sb_unit_tag:  #### Check that the container is not empty (tag is associated with concept)
            pass
        else:
            gem_Or["MapUnit"] = sb_unit_tag["unit_label_abbreviation"]  
            gem_Or["Label"] = PT.getUnitLabel(sb_unit_tag) ### use FGDC font
        
    else: pass
    
    gem_Or["OrientationConfidenceDegrees"] = PT.getOrConfidence(sb_orientation_dict)
    
    return gem_Or 
    
def StraboToMapUnitPoints(sb_point_dict): #### Incomplete
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single point feature dictionary with Strabo attributes
     
    gem_MUP = dict()
    gem_MUP = {
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "",
        "IdendityConfidence" : "",
        "ExistenceConfidence" : "",
        "LocationConfidenceMeters" : "",
        "PlotAtScale" : "",
        "DataSourceID" : "",
        "LocationSourceID" : "",
        "Notes" : ""}
    
    
    # index = CONFIG.PT_SB.index(sb_orientation_str)
    # gem_MUP["Symbol"]  = CONFIG.PT_Gem_Symbol[index]  
    # gem_MUP["Type"] = CONFIG.PT_Gem_Type[index]
    
    gem_MUP["MapUnit"] = sb_point_dict["ru_unit_label_abbreviation"]
    gem_MUP["Label"] = PT.getUnitLabel(sb_point_dict) ### use FGDC font
    gem_MUP["Symbol"] = sb_point_dict["ru_unit_label_abbreviation"] ### consider subdivision for subscripts
        
    #### maybe use these????
    #gem_MUP["IdentityConfidence"] = LT.getIdentity(sb_point_dict)      
    #gem_MUP["ExistenceConfidence"] = LT.getExistence(sb_point_dict)
    #gem_MUP["LocationConfidenceMeters"] = LT.getLocation(sb_point_dict)
    
    gem_MUP["Notes"] = "Notes: " + sb_point_dict.get("notes", "")
        
    return gem_MUP

def StraboToMapUnitPolyLabels(sb_point_dict): ### Check "symbol"
    ## Builds GeMS style dictionary and completes translation for each field
    ## Takes in a single point feature dictionary with Strabo attributes
     
    gem_MUPL = dict()
    gem_MUPL = {
        "MapUnit" : "",
        "Label" : "",
        "Symbol" : "",
        "IdendityConfidence" : "",
        "DataSourceID" : "",
        "LocationSourceID" : ""}
    
    
    sb_unit_tag, _ = getUnitTag(sb_point_dict)
    
    gem_MUPL["MapUnit"] = sb_unit_tag["unit_label_abbreviation"]  
    
    gem_MUPL["Label"] = PT.getUnitLabel(sb_unit_tag) ### use FGDC font
    gem_MUPL["Symbol"] = sb_unit_tag["unit_label_abbreviation"]   ### consider subdivision for subscripts
    
    
    return gem_MUPL
      
def getUnitTag(sb_dict):
    #Takes in Strabo dict and returns the a Tag dict of the FIRST geologic unit
    unit_dict = dict()
    number_tags = []
    
    if "tags" in sb_dict.keys():
        sb_tags = sb_dict.get("tags")
        number_tags = len(sb_tags)
        for x in range(0, len(sb_tags)):
            if "geologic_unit" in sb_tags[x].get("type"):
                unit_dict = sb_tags[x]
            else: pass
        
    
    return unit_dict, number_tags
