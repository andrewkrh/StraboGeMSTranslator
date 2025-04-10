# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:59:30 2024

@author: ahoxey
"""

######### Point Feature Attribute Translation Functions ############
#### All attribute language is defined within the functions below
#### and called by other modules.
####
####  !!!! IMPORTANT !!!!!!!
#### Custom edits for attribute language or field mapping should be dones here
#### All functions return strings that correspond to GeMS attributes


def getSamType(sb_dict): #### Incomplete
    #### Takes Strabo dictionary and reads attributes for Sample data
    # field sample	
    # soils analysis
    # water chemistry	
    # XRD

    gm_sample_type = "field sample"
    return gm_sample_type


def getUnitLabel(sb_tag_dict): #### Mostly complete - extend for Proterozoic/Archean; Era modification?
    ##### Takes spot data and returns label with FGDC font (eg. Pzu ==> |u)
    sb_abbrev = sb_tag_dict.get("unit_label_abbreviation")
    gm_label = ""
    modifier = ""
    
    tag_str = ""    
    for n in sb_tag_dict:
        if n != "type" and n != "name" and n != "unit_label_abbreviation" and n != "map_unit_name" and n != "rock_type" and n != "id" and n != "continuousTagging":
            if isinstance(sb_tag_dict[n], list):
                temp_str = ' '.join(sb_tag_dict[n])
                tag_str = tag_str + temp_str + " "
            else:
                tag_str = tag_str + sb_tag_dict[n] + " "
        else: None
    
    
    if "paleogene" in tag_str:
        modifier = ":"
        gm_label = sb_abbrev.replace("P", modifier)
    elif "triassic" in tag_str:
        modifier = "^"
        gm_label = sb_abbrev.replace("Tr", modifier)
    elif "pennsylvanian" in tag_str:
        modifier = "*"
        gm_label = sb_abbrev.replace("P", modifier)
    elif "cambrian" in tag_str:
        modifier = "_"
        gm_label = sb_abbrev.replace("C", modifier)
    elif "precambrian" in tag_str:
        modifier = "="
        gm_label = sb_abbrev.replace("PC", modifier)
    else: gm_label = sb_abbrev
    
        
    # elif "proterozoic" in tag_str: ### Several modifiers for Late, Middle, Middle middle, etc...
    #     if ""
        # Precambrian, =
        # Proterozoic, <
        # Late Middle Proterozoic, `
        # Middle Middle Proterozoic, ~
        # Early Middle Proterozoic, !
        # Late Early Proterozoic, @
        # Middle Early Proterozoic, #
        # Early Early Proterozoic, $
        # Pre-Archean, >
    
    return gm_label    


def getOrType(sb_or_str, gm_OrSym): #### Mostly complete - consider using symbol instead of string
    #### Takes Strabo dictionary of orientations data and returns orientation type
    gm_OrType = ""
    
    #Digit 1
    if "fault" in sb_or_str: 
        gm_OrType = "fault"   #### Faults
    elif "joint" in sb_or_str:
        gm_OrType = "joint"   #### Joints
    elif "fold hinge" in sb_or_str:
        gm_OrType = "fold hinge"   #### Fold
    elif "foliation" in sb_or_str:
        gm_OrType = "foliation"   #### Foliation
    elif "mineral alignment" in sb_or_str: 
        gm_OrType = "mineral lineation"   #### Lineation
    elif "slickenlines" in sb_or_str: 
        gm_OrType = "slickenline"   
    elif "bedding" in sb_or_str: 
        gm_OrType = "bedding"   
    else: gm_OrType = "undefined"
     
    # anticline
    # bedding	
    # crenulation lineation	
    # cumulate foliation	
    # dike inclination
    # eolian
    # fault
    # fault decoration
    # fault inclination
    # fault offset	
    # fluvial	
    # fold decoration	
    # fold hinge	
    # foliation	
    # groundwater movement	
    # intersection lineation	
    # joint	
    # landslide	
    # lineation	
    # local fault offset
    # mineral lineation
    # minor fault
    # minor fold	
    # modern current
    # overturned bedding
    # paleocurrent
    # plunge
    # primary foliation
    # secondary foliation
    # slickenline
    # spring
    # stretching lineation
    # syncline
    # Toreva block    
    
    return gm_OrType


def getOrSymbol(sb_or_str): #### Incomplete; Many more potential options
    ## Consider taking in gm_type (post type translation) rather than getting sb_type 
    ## FGDC symbol schematic is very different from Strabo attribute schematic
    
    
    
    # gm_OrSym = 0
    
    # if "planar" in sb_or_str:
    #     None
    # elif "linear" in sb_or_str:
    #     None
    # else:None
    
    # if "bedding" in sb_or_str:
    #     gm_OrSym = 600
        
        
        
    # if "cleavage" in sb_or_str:
    #     gm_OrSym = 700


    # if "foliation" in sb_or_str:
    #     gm_OrSym = 8100        # general
    #     if "igneous" in sb_or_str:
    #         gm_OrSym = 8200        # igneous
    #     if "metamorphic" in sb_or_str:
    #         gm_OrSym = 8200        # metamorphic
        
        
    # if "lineation" in sb_or_str:
    #     gm_OrSym = 900
        
    # if "horizontal" in sb_or_str:
    #     gm_OrSym = gm_OrSym + 1
    # elif "vertical" in sb_or_str:
    #     gm_OrSym = gm_OrSym + 3
    # elif "overturned" in sb_or_str:
    #     gm_OrSym = gm_OrSym + 4
    # else:
    #     gm_OrSym = gm_OrSym + 2
        
        
        
    #Digit 1
    if "fault" in sb_or_str: 
        gm_OrSym = "02.11."   #### Faults
    elif "joint" in sb_or_str:
        gm_OrSym = "04.03."   #### Joints
    elif "fold hinge" in sb_or_str:
        gm_OrSym = "05.11."   #### Fold
    elif "bedding" in sb_or_str:
        gm_OrSym = "06."   #### Bedding
    elif "foliation" in sb_or_str:
        gm_OrSym = "08.01."   #### Foliation
    elif "mineral alignment" in sb_or_str: 
        gm_OrSym = "09.001"   #### Lineation
    elif "slickenlines" in sb_or_str: 
        gm_OrSym = "09.017"   #### Lineation

    else: gm_OrSym = "31." #### Make a 31.01.01 default symbol that turns lines red;
        
    #Digit 3    ### this may not apply to all measurements
    if "upright" in sb_or_str:
        gm_OrSym = gm_OrSym + "02"
    elif "overturned" in sb_or_str:
        gm_OrSym = gm_OrSym + "04"
    else: 
        gm_OrSym = gm_OrSym + "01"
    
    return gm_OrSym


def getOrConfidence(sb_orientation_dict): 
    #### return confidenc in *degrees*
    sb_quality = sb_orientation_dict.get("quality", str(5)) ## 1-5; 5 excellent (default)
    gm_OrCon = 15//int(sb_quality)
    
    return gm_OrCon 






