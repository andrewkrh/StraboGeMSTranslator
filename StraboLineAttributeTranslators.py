# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:00:43 2024

@author: ahoxey
"""

######### Linear Feature Attribute Translation Functions ############
#### All attributes are defined within the functions below, respectively,
#### and called by other modules.
####
####  !!!! IMPORTANT !!!!!!!
#### Custom edits for attribute language or field mapping should be done in getSymbol.
#### By default, all the GeMS attributes are determined according to their FDGC Symbol.
#### Modifactions beyond the FDGC Symbols can be made within the subsiquent functions
#### All functions return strings that correspond to GeMS attributes

# from difflib import SequenceMatcher
# from strsimpy.jaro_winkler import JaroWinkler


import sys
import os
appcwd = os.getcwd()
fuzz_module = appcwd + "/resources/fuzzywuzzy-master"
sys.path.append(fuzz_module)
from fuzzywuzzy import fuzz

import StraboGEMConfig as CONFIG
global CONFIG



def getSymbol(sb_line_str):  ### Mostly complete - Several FGDC lines not included 
    ## Builds a string
    ## Takes in a STRING with Strabo Line description to calcualte FGDC symbol
    ## Calculates an integer based on line type, then converts int to string with '.'
    
    GEMSymbol = 0
    
    ## Starbo Menu Contacts
    if "contact" in sb_line_str or "bedding" in sb_line_str:
        GEMSymbol = GEMSymbol + 10100

        if "unconformity" in sb_line_str:
            GEMSymbol = GEMSymbol + 24
        elif "bedding" in sb_line_str:
            GEMSymbol = GEMSymbol + 8
        elif "gradational" in sb_line_str:
            GEMSymbol = GEMSymbol + 16
        elif "volcanic"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 723 ### adds to contact 100
        elif "marker_layer" in sb_line_str:
            GEMSymbol = GEMSymbol + 100 ### adds to contact 100
            if "clay" in sb_line_str:
                GEMSymbol = GEMSymbol + 8
            if "economic" in sb_line_str:
                GEMSymbol = GEMSymbol + 16
            if "coal" in sb_line_str:
                GEMSymbol = GEMSymbol + 24
            if "clinker" in sb_line_str:
                GEMSymbol = GEMSymbol + 32
            else: None
        else: None
    else: None
    
    ## Starbo Menu Igneous contacts
    if "dike" in sb_line_str:
        GEMSymbol = GEMSymbol + 200 ## adds to 100 for contact
    else: None     
    
    
    ## Starbo Menu 6 (faults)    
    if "fault" in sb_line_str:
        GEMSymbol = GEMSymbol + 20000
        if "dextral"  in sb_line_str and "normal" not in sb_line_str and "reverse" not in sb_line_str:  
            GEMSymbol = GEMSymbol + 600
        elif "sinistral"  in sb_line_str and "normal" not in sb_line_str and "reverse" not in sb_line_str:  
            GEMSymbol = GEMSymbol + 608
        elif "nomal"  in sb_line_str  and "low_angle" not in sb_line_str and "sinistral" not in sb_line_str and "dextral" not in sb_line_str:
            GEMSymbol = GEMSymbol + 200
        elif "low_angle_norm"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 1000
        elif "reverse"  in sb_line_str and "sinistral" not in sb_line_str and "dextral" not in sb_line_str:  
            GEMSymbol = GEMSymbol + 400
        elif "thrust"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 800
        elif "dextral_reverse"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 700
        elif "dextral_normal"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 700
        elif "sinistral_reverse"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 708
        elif "sinistral_normal"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 708
        else: GEMSymbol = GEMSymbol + 100
    else: None
    
    if "fault" in sb_line_str and "scarp" in sb_line_str:
        GEMSymbol = 1200
        
    
    
    ## Starbo Menu 7 (folds)    
    if "fold_axial_tra" in sb_line_str:
        GEMSymbol = GEMSymbol + 50000
        if "syncline"  in sb_line_str:
            GEMSymbol = GEMSymbol + 500
        elif "anticline"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 100
        elif "monocline"  in sb_line_str:
            GEMSymbol = GEMSymbol + 900
        elif "antiformal_syn"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 732
        elif "synformal_anti"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 332
        elif "synform"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 600
        elif "antiform"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 200
        elif "s_fold" in sb_line_str or "z_fold" in sb_line_str or "m_fold" in sb_line_str:  
            GEMSymbol = GEMSymbol + 1100
        elif "ptygmatic"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 1000
        elif "unknown"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 1000
        else: None
    else: None
    
    if "sheath" in sb_line_str:
        GEMSymbol = GEMSymbol + 200       
    else: None
    
    #Strabo Menu 8 (Geomorphic) #### These are not uniform and are likely incorrect
    if "geomorphic_fea" in sb_line_str:
        GEMSymbol = 11000
        if "glacial" in sb_line_str:
            GEMSymbol = GEMSymbol + 300
        elif "fluvial"  in sb_line_str:
            GEMSymbol = GEMSymbol + 200
        elif "marine"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 500
        elif "lacustine" in sb_line_str:
            GEMSymbol = GEMSymbol + 500
        elif "arid"  in sb_line_str:
            GEMSymbol = GEMSymbol + 600
        elif "debris"  in sb_line_str:
            GEMSymbol = GEMSymbol + 700
        elif "landslide"  in sb_line_str:
            GEMSymbol = GEMSymbol + 700
        elif "volcanic"  in sb_line_str: ### recycle line quality?
            GEMSymbol = GEMSymbol + 801
        else: None       
        if "ridge" in sb_line_str:
            GEMSymbol = GEMSymbol + 10
        elif "shoreline"  in sb_line_str:
            GEMSymbol = GEMSymbol + 13
        elif "scarp"  in sb_line_str:  
            GEMSymbol = GEMSymbol + 00
        else: None
    else: None

    #Strabo Menu 9 (Anthropogenic)
    if "anthropenic_fe" in sb_line_str:
        GEMSymbol = 12800
        if "fence_line" in sb_line_str:
            GEMSymbol = GEMSymbol + 107   
        if "property_line" in sb_line_str:
            GEMSymbol = GEMSymbol + 106      
        if "road" in sb_line_str:
            GEMSymbol = GEMSymbol + 2
        if "trail" in sb_line_str:
            GEMSymbol = GEMSymbol + 15
        if "other" in sb_line_str: ### makes railroad
            GEMSymbol = GEMSymbol + 19
        else: None
    else: None

            
    ## Starbo Menu 1 (final Digit)
    if "known" in sb_line_str:
        GEMSymbol = GEMSymbol + 1
    elif "approximate"  in sb_line_str and "approximate(?)" not in sb_line_str:
        GEMSymbol = GEMSymbol + 3
    elif "approximate(?)"  in sb_line_str:  
        GEMSymbol = GEMSymbol + 4
    elif "inferred"  in sb_line_str and "inferred(?)" not in sb_line_str:
        GEMSymbol = GEMSymbol + 5
    elif "inferred(?)"  in sb_line_str:
        GEMSymbol = GEMSymbol + 6
    elif "concealed"  in sb_line_str:
        GEMSymbol = GEMSymbol + 7 
    else:
        GEMSymbol = GEMSymbol + 31
    
    
    ### Convert to String
    def insert_char(string, index, char):
        return string[:index] + char + string[index:]
    
    GEMSymbol = str(GEMSymbol)
    GEMSymbol = insert_char(GEMSymbol, 0, "0")
    GEMSymbol = insert_char(GEMSymbol, 2, ".")
    GEMSymbol = insert_char(GEMSymbol, 5, ".")
    
    if "anthropenic_fe" in sb_line_str or "geomorphic_fea" in sb_line_str:
        GEMSymbol = GEMSymbol[3:]
 

    #Special cases
    if "deformation_zo" in sb_line_str:
        GEMSymbol = "14.02"
    if "shear_zone" in sb_line_str:
        GEMSymbol = "14.01"
    if "plunging" in sb_line_str and "anticline" in sb_line_str:
        GEMSymbol = "05.10.05"
    if "plunging" in sb_line_str and "syncline" in sb_line_str:
        GEMSymbol = "05.10.06"
    if "other_feature"  in sb_line_str and "extent_of_map" in sb_line_str:  
        GEMSymbol = "31.08"  
    if "cross_section" in sb_line_str:
        GEMSymbol = "31.10"
    if "stratigraphic_section" in sb_line_str:             
        GEMSymbol = "31.05"

    return GEMSymbol

def getType(sb_line_str, gm_symbol): #### Mostly complete - consider using ArcRULEs 
    #### Takes in a line string and GeMS symbol and returns line type
    #### Relies on TheFuzz module for string comparison and 'best' match
    #### Includes customizations to avoid common problems associated with TheFuzz
    
    
    #### Deals with obvious problems that arise from Fuzz string similarity
    Options = CONFIG.LN_Type_options
    while("fault scarp" in Options):
        Options.remove("fault scarp") #temporarily remove fault scarp as an option
    sb_str = sb_line_str.replace("sinistral", "left-lateral")
    sb_str = sb_line_str.replace("dextral", "right-lateral")
    sb_str = sb_line_str.replace("marker_layer", "key bed")
    
    ### Get description based on symbols
    default = {"Description": "No description found"}
    FGDC_description = CONFIG.FGDC_Symbol_Table.get(gm_symbol, default).get("Description")   
    
    #### Compare description strings (GeMS type vs FGDC vs Strabo)
    #initial (FDGC vs GeMS; returns top 3 matches)
    ratio_list = []
    for x in range(0, len(CONFIG.LN_Type_options)):
        sample_ratio = []
        sample_ratio = fuzz.ratio(FGDC_description[:10], Options[x]) #only compares with first 10 chars in description
        ratio_list.append(sample_ratio)
    highest_ratio = sorted(ratio_list, reverse=True)
    highest_ratio = highest_ratio[:3]
    
    # Get GeMS type
    index_list = []
    best_matches = []
    for n in range(0, len(highest_ratio)):
        index_list.append(ratio_list.index(highest_ratio[n]))
        temp_type = CONFIG.LN_Type_options[index_list[n]]
        best_matches.append(temp_type)
     
    # Compare top results (GeMS to Strabo)
    top_ratio_list = []
    for m in range(0, len(best_matches)):
        sample_ratio = []
        sample_ratio = fuzz.ratio(sb_str[-20:], best_matches[m]) #only compares with final 20 chars in SB String
        top_ratio_list.append(sample_ratio)
    
    # Get final type
    index = top_ratio_list.index(max(top_ratio_list))
    GEMType = best_matches[index]
    
    # Reset if no symbol assigned
    if "No description" in FGDC_description:
        GEMType = "miscellaneous map element"
    else:None
        
    return GEMType     

def getCFType(sb_line_str, gm_symbol): #### REMOVE
    #### Takes in a strabo dictionary and reads attributes for Contacts&Faults line type
    
    DigitA = gm_symbol[:2]
    DigitB = gm_symbol[3:4]
    DigitC = gm_symbol[-2:]
    
    ##### First Digit
    if DigitA == "01":
        GEMType = "contact"
        
    elif DigitA =="02":
        GEMType = "fault"
        
        
    elif DigitA =="05":
        GEMType = "fold"
    
    else: GEMType = "undefined"
    
    
    
    # ######################## Consider deleting
    # if "contact" in sb_line_str:
    #     #contact
    #     #igneous contact
    #     #intrusive contact
    #    #metamorphic contact
    #    #internal contact
    #    #angular unconformity
    #    #disconformity
    #    #nonconformity
    #    #paraconformity
    #    #unconformity                                                                 
    #     sb_contact_type = sb_dict["tr_contact_type"]                                                        
    #     if sb_contact_type == "depositional":
    #         GEMType = "contact"                                                               
    #     elif sb_contact_type == "intrusive":
    #         GEMType = "intrusive contact"
    #     elif sb_contact_type == "metamorphic":
    #         GEMType = "metamorphic contact"
    #     elif sb_contact_type == "other":
    #         GEMType = "contact"                                                               
                                                               
    # elif sb_line_str == "geologic structure":
    #     sb_struct_type = sb_dict["tr_geologic_structure_type"]
    #     sb_shear_sense = sb_dict["tr_shear_sense"]
    # #fault
    # #normal fault
    # #thrust fault
    # #reverse fault
    # #right-lateral strike-slip fault
    # #left-lateral strike-slip fault
    # #right-lateral oblique-slip fault
    # #left-lateral oblique-slip fault
    # #detachment fault
    # #low-angle normal fault
    
                
    #             ### Additional GEM Types that could be added
    #             #fault scarp
    #             #scarp  
    #             #elevation profile
    #             #eolian
    #             #escarpment
    #             #geophysical fault
    #             #gradational contact
    #             #headscarp
    #             #joint
    #             #breccia
    #             #miscellaneous map element 
    #             #map boundary

        
        
        
    return GEMType        
            
def getGLType(sb_line_str, gm_symbol): #### REMOVE
    #### Takes in a strabo dictionary and reads attributes for Geologic Lines line type
    
    
    DigitA = gm_symbol[:2]
    DigitB = gm_symbol[3:4]
    DigitC = gm_symbol[-2:]
    
    ##### First Digit
    if DigitA == "01":
        GEMType = "contact"
        
    elif DigitA =="02":
        GEMType = "fault"
        
        
    elif DigitA =="05":
        GEMType = "fold"
    
    else: GEMType = "undefined"
    
    
    
    
    
    # if "tr_structure_type" in sb_dict.keys():
    #     sb_struct_type = sb_dict["tr_structure_type"]
    #     if sb_struct_type == "syncline":
    #         GEMType = "syncline"
    #     elif sb_struct_type == "anticline":
    #         GEMType = "antincline"
    #     elif sb_struct_type == "monocline":
    #         GEMType = "monocline"
    #     elif sb_struct_type == "syncline":
    #         GEMType = "syncline"
    #     elif sb_struct_type == "antiformal_syn":
    #         GEMType = "syncline"
    #     elif sb_struct_type == "antiformal_ant":
    #             GEMType = "antincline"
    #     else: GEMType = "undefined fold"

    # if "tr_geomorohic_type" in sb_dict.keys():
    #     sb_geomorphic_type = sb_dict["tr_geomorphic_type"]
    #     if sb_geomorphic_type == "syncline":
    #         GEMType = "syncline"
    #     elif sb_geomorphic_type == "anticline":
    #         GEMType = "antincline"
    # else:
    #         GEMType = "Null"
    #         #contact
    #         #igneous contact
    #         #intrusive contact
    #         #metamorphic contact
    #         #internal contact
    #         #angular unconformity
    #         #disconformity        
    return GEMType        

def getMULType(sb_line_str, gm_symbol): #### REMOVE
    #### Takes in a strabo dictionary and reads attributes for Contacts&Faults line type
    
    DigitA = gm_symbol[:2]
    DigitB = gm_symbol[3:4]
    DigitC = gm_symbol[-2:]
    
    ##### First Digit
    if DigitA == "01":
        GEMType = "contact"
        
    elif DigitA =="02":
        GEMType = "fault"
        
        
    elif DigitA =="05":
        GEMType = "fold"
    
    else: GEMType = "undefined"
    
    
    
    # if "tr_marker_layer_details" in sb_dict.keys():
    #     GEMType = "marker bed"
        
    # elif "tr_contact_type" == "intrusive":
    #     GEMType = sb_dict.get("tr_intrusive_contact_type")
    # else: GEMType = "Unknown"        
    
    
    
    return GEMType  

def getIdentity(sb_line_str, gm_symbol): ## Uses SB Str; Consider changing to use symbol
    #analytical
    #certain
    #questionable
    #unspecified
    
    # DigitA = gm_symbol[:2]
    # DigitB = gm_symbol[3:4]
    # DigitC = gm_symbol[-2:]
    
    # if DigitC == "01":
    #     GEMIdentity = "certain"
    # elif DigitC =="02":
    #     GEMIdentity = "questionable"
    
    if "known" in sb_line_str:
        GEMIdentity = "certain"
    elif "approximate"  in sb_line_str and "approximate(?)" not in sb_line_str:
        GEMIdentity = "certain"
    elif "approximate(?)"  in sb_line_str:  
        GEMIdentity = "questionable"
    elif "inferred"  in sb_line_str and "inferred(?)" not in sb_line_str:
        GEMIdentity = "certain"
    elif "inferred(?)"  in sb_line_str:
        GEMIdentity = "questionable"
    elif "concealed"  in sb_line_str:
        GEMIdentity = "certain"
    else:
        GEMIdentity = "certain"
        
    return GEMIdentity

def getExistence(sb_line_str, gm_symbol): ## Uses SB Str; Consider changing to use symbol
    #analytical
    #certain
    #questionable
    #unspecified
    
    # DigitA = gm_symbol[:2]
    # DigitB = gm_symbol[3:4]
    # DigitC = gm_symbol[-2:]
    
    # ##### First Digit
    # if DigitC == "01":
    #     GEMExistence = "certain"
        
    # elif DigitC =="02":
    #     GEMExistence = "questionable"
        
    # elif DigitC =="05":
    #     GEMExistence = "analytical"
    
    # else: GEMExistence = "undefined"
    
    
    if "known" in sb_line_str:
        GEMExistence = "certain"
    elif "approximate"  in sb_line_str and "approximate(?)" not in sb_line_str:
        GEMExistence = "certain"
    elif "approximate(?)"  in sb_line_str:  
        GEMExistence = "questionable"
    elif "inferred"  in sb_line_str and "inferred(?)" not in sb_line_str:
        GEMExistence = "certain"
    elif "inferred(?)"  in sb_line_str:
        GEMExistence = "questionable"
    elif "concealed"  in sb_line_str:
        GEMExistence = "certain"
    else:
        GEMExistence = "certain"
              
    return GEMExistence

def getConcealed(sb_line_str, gm_symbol): ## Complete; should not use symbol!!! 
    #y
    #n
    
    if "concealed"  in sb_line_str:
        GEMConcealed = "y"
    else:
        GEMConcealed = "n"
        
    # DigitC = gm_symbol[-2:]
    
    # if DigitC == "07":
    #     GEMConcealed = "y"
    # else:
    #     GEMConcealed = "n"
              
    return GEMConcealed

def getLocation(sb_line_str, gm_symbol): ## Complete; should not use symbol!!! 
    #5
    #50
    #100
    
    if "known" in sb_line_str:
        GEMLocation = 5
    elif "approximate"  in sb_line_str and "approximate(?)" not in sb_line_str:
        GEMLocation = 50
    elif "approximate(?)"  in sb_line_str:  
        GEMLocation = 50
    elif "inferred"  in sb_line_str and "inferred(?)" not in sb_line_str:
        GEMLocation = 50
    elif "inferred(?)"  in sb_line_str:
        GEMLocation = 50
    elif "concealed"  in sb_line_str:
        GEMLocation = 100
    else:
        GEMLocation = 5
        
    
    # DigitC = gm_symbol[-2:]
    
    # if DigitC == "01":
    #     GEMLocation = 5
    # elif DigitC == "02":
    #     GEMLocation = 5
    # elif DigitC ==  "03":
    #     GEMLocation = 50
    # elif DigitC == "04":
    #     GEMLocation = 50
    # elif DigitC == "07":
    #     GEMLocation = 100
    # else:
    #     GEMLocation = 100
              
    return GEMLocation
