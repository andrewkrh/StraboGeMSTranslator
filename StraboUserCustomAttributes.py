#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:04:11 2024

@author: andrewhoxey
"""

########### Custom User Functions  #############
import StraboGEMConfig as CONFIG
global CONFIG


# #### Line Features #####
def SortLineFeature_custom(sb_trace_str):
    #### Decision tree that sorts through strabo line characterizations
    #### Takes TraceFeature.get["properties"]
    #### 1 = ContactsAndFaults; 2 = GeologicLines; 3 = MapUnitLines; 4 = CartographicLines; 5 = Default Unsorted
        
    index = CONFIG.LN_SB.index(sb_trace_str)
    tempSort = CONFIG.LN_Gem_Sort[index]
    
    if tempSort == "ContactsAndFaults":
        Sort = 1
    elif tempSort == "GeologicLines":
        Sort = 2
    elif tempSort == "MapUnitLines":
        Sort = 3
    elif tempSort == "CartographicLines":
        Sort = 4
    else: Sort = 5
        
    return Sort

def getSymbol_custom(sb_line_str): 
    
    index = CONFIG.LN_SB.index(sb_line_str)
    gm_symbol = CONFIG.LN_Gem_Symbol[index]
    
    return gm_symbol
    
def getLineType_custom(sb_line_str, gm_symbol):
    #### Takes in a strabo dictionary and reads attributes for Contacts&Faults line type
    ### Read dict
    temp_type = ""
    
    UsingKeys = ([k for k in Feature.keys() if 'tr' in k])
    if "tr_trace_feature" in UsingKeys:
        UsingKeys.remove("tr_trace_feature")
    else: None
    
    for n in range(0, len(UsingKeys)):
        search = UsingKeys[n]
        temp_type = temp_type + Feature.get(search) +" "
        
    index = CONFIG.LN_SB.index(temp_type)
    gm_type = CONFIG.LN_Gem_Type[index]
    
    return gm_type
    
#### Point Features #####
def SortPoint_custom(Feature): #### Incomplete; Never used in StraboUtils
    ### Change for "po_feature"
    #### Decision tree that sorts through strabo point characterizations
    #### 1 = Stationns; 2 = GenericSamples; 3 = OrientationPoints; 4 = MapUnitPoints; 5 = MapUnitPolyLabels;
        
    temp_type = ""
    temp_type = Feature["feature_type"] + " " + Feature["facing"] + " " + Feature["facing_defined_by"] + " " + "quality-" + str(Feature["quality"]) + " " + Feature["notes"]
        
    index = CONFIG.LN_SB.index(temp_type)
    tempSort = CONFIG.LN_Gem_Sort[index]
    
    if tempSort == "Stations":
        Sort = 1
    elif tempSort == "GenericSamples":
        Sort = 2
    elif tempSort == "OrientationPoints":
        Sort = 3
    elif tempSort == "MapUnitPoints":
        Sort = 4
    else: Sort = 5
        
    return Sort

def getPointType_custom(Feature):
    #### Takes in a strabo dictionary and reads attributes for Custom Orientation type
    temp_type = ""
    temp_type = Feature["feature_type"] + " " + Feature["facing"] + " " + Feature["facing_defined_by"] + " " + "quality-" + str(Feature["quality"]) + " " + Feature["notes"]

    index = CONFIG.PT_SB.index(temp_type)
    gm_type = CONFIG.PT_Gem_Type[index]

    return gm_type

def getOrSymbol_custom(Feature): #### Incomplete; Consider making
    temp_type = ""
    temp_type = Feature["feature_type"] + " " + Feature["facing"] + " " + Feature["facing_defined_by"] + " " + "quality-" + str(Feature["quality"]) + " " + Feature["notes"]

    index = CONFIG.PT_SB.index(temp_type)
    gm_sym = CONFIG.PT_GEM_Symbol[index]    

    return gm_sym