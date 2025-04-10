# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:03:27 2024

@author: ahoxey
"""

import StraboGEMTranslator as SGT
import StraboUtils as SU
import StraboGEMConfig as CONFIG

import StraboLineAttributeTranslators as LT
import StraboPointAttributeTranslators as PT

import StraboWorkingConfig as SWC

_, _, found_lines, found_points = SU.ImportStrabo('G:\My Drive\Research\SoftwareScripts\StraboArcTranslation\PythonScripts\JSONTestFiles\TestA_LaPlata_2024-11-14_1020pm__20240901.json')



PointList = [{
    "geometry": {
        "type": "Point",
        "coordinates": [
            -108.1903582913516,
            36.92889111243811
        ]
    },
    "properties": {
        "date": "2024-08-15T20:00:13.000Z",
        "viewed_timestamp": 1723752013605,
        "notes": "Test Spot;\nPost Office",
        "modified_timestamp": 1723752045582,
        "symbology": {
            "circleColor": "transparent"
        },
        "name": "LaPlata_AH_01",
        "samples": [
                   {
                       "sample_id_name": "LaPlata_AH_2580",
                       "inplaceness_of_sample": "5___definitely",
                       "oriented_sample": "no",
                       "sample_description": "Vein along fault in Kch",
                       "id": 17434457982230
                   }
               ],
        "notesTimestamp": "Thu Aug 15 2024 14:00:45 GMT-0600 (Mountain Daylight Time)",
        "time": "2024-08-15T20:00:13.000Z",
        "id": 17237520136055,
        "self": "https:\/\/strabospot.org\/db\/feature\/17237520136055"
    },
    "type": "Feature"
},
{
    "geometry": {
        "type": "Point",
        "coordinates": [
            -108.2363259888344,
            36.91410243695381
        ]
    },
    "properties": {
        "date": "2024-08-23T21:52:11.000Z",
        "viewed_timestamp": 1724449931665,
        "symbology": {
            "circleColor": "transparent"
        },
        "name": "LaPlata_AH_02",
        "time": "2024-08-23T21:52:11.000Z",
        "id": 17244499316640,
        "modified_timestamp": 1724701402433,
        "self": "https:\/\/strabospot.org\/db\/feature\/17244499316640"
    },
    "type": "Feature"
},
{
    "geometry": {
        "type": "Point",
        "coordinates": [
            -108.1903430515668,
            36.92865893718431
        ]
    },
    "properties": {
        "date": "2024-08-23T23:02:00.000Z",
        "viewed_timestamp": 1724454120829,
        "notes": "Post office 2",
        "orientation_data": [],
        "modified_timestamp": 1724862064536,
        "symbology": {
            "circleColor": "transparent"
        },
        "name": "LaPlata_AH_3",
        "notesTimestamp": "Fri Aug 23 2024 17:02:19 GMT-0600",
        "time": "2024-08-23T23:02:00.000Z",
        "id": 17244541208291,
        "self": "https:\/\/strabospot.org\/db\/feature\/17244541208291"
    },
    "type": "Feature"
},
{
    "properties": {
        "images": [
            {
                "width": 4096,
                "id": 17247783465270,
                "modified_timestamp": 1725040241173,
                "image_type": "sketch",
                "height": 1606,
                "annotated": False,
                "self": "https:\/\/strabospot.org\/db\/image\/17247783465270"
            },
            {
                "width": 4096,
                "id": 17247782972206,
                "modified_timestamp": 1725040240569,
                "height": 1606,
                "annotated": False,
                "self": "https:\/\/strabospot.org\/db\/image\/17247782972206"
            }
        ],
        "date": "2024-08-27T16:46:00.000Z",
        "altitude": 1999.8032779694,
        "viewed_timestamp": 1724777160019,
        "notes": "Pome lookout;\ncoal throughout; \nfluvial interbedded with muds;\npetrified wood and bones above picketed cliffs;\nend of marine;\n\"clinker\" metasomatized mudstone from burning coal seam\n\nLauentana",
        "modified_timestamp": 1725555126360,
        "gps_accuracy": 3.5355339059327,
        "name": "LaPlata_AH_5",
        "notesTimestamp": "Thu Sep 05 2024 10:52:06 GMT-0600 (Mountain Daylight Time)",
        "time": "2024-08-27T16:46:00.000Z",
        "id": 17247771600198,
        "self": "https:\/\/strabospot.org\/db\/feature\/17247771600198",
        "tags": [
            {
                "type": "geologic_unit",
                "name": "Kmf - Menefee Formation",
                "unit_label_abbreviation": "Kmf",
                "map_unit_name": "Menefee Formation",
                "rock_type": "sedimentary",
                "sedimentary_rock_type": "sandstone",
                "eon": [
                    "phanerozoic"
                ],
                "era_phanerozoic": [
                    "mesozoic"
                ],
                "period_mesozoic": [
                    "cretaceous"
                ],
                "age_modifier": [
                    "late"
                ],
                "notes": "Mesaverde Group",
                "id": 17236591897571,
                "color": "#00CC00",
                "description": "Terrestrial mudsand",
                "continuousTagging": False
            }
        ]
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -106.9654754363997,
            35.84572599272788
        ]
    },
    "type": "Feature"
},
{
    "geometry": {
        "type": "Point",
        "coordinates": [
            -106.9749349779302,
            35.87781508244274
        ]
    },
    "properties": {
        "date": "2024-08-27T17:13:31.000Z",
        "altitude": 2016.027720985,
        "viewed_timestamp": 1724778811779,
        "notes": "Levantine\n\nLewis shale\nInterfingering",
        "modified_timestamp": 1724778881746,
        "gps_accuracy": 4.7986027929747,
        "name": "LaPlata_AH_6",
        "notesTimestamp": "Tue Aug 27 2024 11:14:41 GMT-0600",
        "time": "2024-08-27T17:13:31.000Z",
        "id": 17247788117792,
        "self": "https:\/\/strabospot.org\/db\/feature\/17247788117792"
    },
    "type": "Feature"
},]

LineList = [{
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [
                -108.1748096281764,
                36.97773964605918
            ],
            [
                -108.1745741029023,
                36.9778632899517
            ],
            [
                -108.1742140856976,
                36.9778525383159
            ],
            [
                -108.1738111055693,
                36.97803661147343
            ],
            [
                -108.1736650526303,
                36.97812519496121
            ],
            [
                -108.1733592714702,
                36.97816509484018
            ],
            [
                -108.1731434652549,
                36.97807130513561
            ],
            [
                -108.1730492785692,
                36.97791241337914
            ],
            [
                -108.1730869290292,
                36.97758643486917
            ],
            [
                -108.1732719846012,
                36.97743859921989
            ],
            [
                -108.1736959300944,
                36.97729076328191
            ],
            [
                -108.1740727705335,
                36.97719130985386
            ],
            [
                -108.1743621301558,
                36.97717787019025
            ],
            [
                -108.1747146330415,
                36.97726603354228
            ],
            [
                -108.174887106453,
                36.97739882000525
            ],
            [
                -108.1749172968728,
                36.97759181070607
            ],
            [
                -108.1748971089923,
                36.97768319986727
            ]
        ]
    },
    "properties": {
        "date": "2024-10-10T19:13:46.000Z",
        "viewed_timestamp": 1728587626486,
        "symbology": {
            "lineColor": "#000000",
            "lineWidth": 2,
            "lineDasharray": [
                5,
                2
            ]
        },
        "trace": {
            "trace_feature": True,
            "trace_quality": "approximate",
            "trace_type": "contact",
            "contact_type": "depositional",
            "depositional_contact_type": "alluvial"
        },
        "name": "LaPlata_AH_775",
        "time": "2024-10-10T19:13:46.000Z",
        "id": 17285876264865,
        "modified_timestamp": 1728589461819,
        "self": "https:\/\/strabospot.org\/db\/feature\/17285876264865",
        "tags": [
            {
                "type": "geologic_unit",
                "name": "Kch - Cliff House Sandstone",
                "unit_label_abbreviation": "Kch",
                "map_unit_name": "Cliff House Sandstone",
                "rock_type": "sedimentary",
                "sedimentary_rock_type": "sandstone",
                "age_modifier": [
                    "late"
                ],
                "notes": "Mesaverde Group",
                "id": 17236590708311,
                "color": "#006600",
                "description": "Marine shoreface",
                "continuousTagging": False
            },
            {
                "type": "geologic_unit",
                "name": "Kmf - Menefee Formation",
                "unit_label_abbreviation": "Kmf",
                "map_unit_name": "Menefee Formation",
                "rock_type": "sedimentary",
                "sedimentary_rock_type": "sandstone",
                "eon": [
                    "phanerozoic"
                ],
                "era_phanerozoic": [
                    "mesozoic"
                ],
                "period_mesozoic": [
                    "cretaceous"
                ],
                "age_modifier": [
                    "late"
                ],
                "notes": "Mesaverde Group",
                "id": 17236591897571,
                "color": "#00CC00",
                "description": "Terrestrial mudsand",
                "continuousTagging": False
            }
        ]
    },
    "type": "Feature"
},
{
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [
                -108.1767196386325,
                36.97607061371176
            ],
            [
                -108.1761088914934,
                36.97628470168441
            ],
            [
                -108.1755599634967,
                36.97655126703339
            ],
            [
                -108.1747229097368,
                36.97672003652988
            ],
            [
                -108.1744231927649,
                36.9765057251017
            ],
            [
                -108.1739185789764,
                36.97692655896485
            ],
            [
                -108.1733003912854,
                36.97698733327873
            ],
            [
                -108.17249831204,
                36.97707558199637
            ],
            [
                -108.1717330547955,
                36.97737869637304
            ]
        ]
    },
    "properties": {
        "date": "2024-10-10T19:16:23.000Z",
        "viewed_timestamp": 1728587783980,
        "symbology": {
            "lineColor": "#000000",
            "lineWidth": 2,
            "lineDasharray": [
                5,
                2
            ]
        },
        "trace": {
            "trace_feature": True,
            "trace_quality": "approximate",
            "trace_type": "contact",
            "contact_type": "marker_layer"
        },
        "name": "LaPlata_AH_776",
        "time": "2024-10-10T19:16:23.000Z",
        "id": 17285877839796,
        "modified_timestamp": 1728592338414,
        "self": "https:\/\/strabospot.org\/db\/feature\/17285877839796",
        "tags": [
            {
                "type": "geologic_unit",
                "name": "Kch - Cliff House Sandstone",
                "unit_label_abbreviation": "Kch",
                "map_unit_name": "Cliff House Sandstone",
                "rock_type": "sedimentary",
                "sedimentary_rock_type": "sandstone",
                "age_modifier": [
                    "late"
                ],
                "notes": "Mesaverde Group",
                "id": 17236590708311,
                "color": "#006600",
                "description": "Marine shoreface",
                "continuousTagging": False
            },
            {
                "type": "geologic_unit",
                "name": "Kmf - Menefee Formation",
                "unit_label_abbreviation": "Kmf",
                "map_unit_name": "Menefee Formation",
                "rock_type": "sedimentary",
                "sedimentary_rock_type": "sandstone",
                "eon": [
                    "phanerozoic"
                ],
                "era_phanerozoic": [
                    "mesozoic"
                ],
                "period_mesozoic": [
                    "cretaceous"
                ],
                "age_modifier": [
                    "late"
                ],
                "notes": "Mesaverde Group",
                "id": 17236591897571,
                "color": "#00CC00",
                "description": "Terrestrial mudsand",
                "continuousTagging": False
            }
        ]
    },
    "type": "Feature"
        }]

LineList = found_lines

testStr = []
testSymbol = []
tempstr=""
tempsym=[]
temp=""
FGDC_description = []

userID = "test"
locID = "tester"


GM_Stations, GM_GenericSamples, GM_OrientationPoints, GM_MapUnitPoints, GM_MapUnitPolyLabels, pt_errors = SU.StraboToGEMPoints(PointList, userID, locID)

print(GM_GenericSamples)



# for x in range(0, len(LineList)):
#     tempstr = ""
#     tempstr = SU.getSBLineTraceString(LineList[x].get("properties"))
#     testStr.append(tempstr)
#     tempsym = ""
#     tempsym = LT.getSymbol(tempstr)
#     testSymbol.append(tempsym)
    


# default = {"Description": "No description found"}


# for n in range(0, len(testSymbol)):
#     temp_str = testSymbol[n]
#     test_description = CONFIG.FGDC_Symbol_Table.get(temp_str, default).get("Description")
#     FGDC_description.append(test_description)

# result = []
# for x in range(0, len(testSymbol)):
#     temp_result = LT.getType(testStr[x], testSymbol[x])
#     result.append(temp_result)

#for m in range(0, len(result)):    
   # print(result[m], FGDC_description[m])

# """
# print(PointDict.get("features"), "I tried")

# featureList = PointDict.get("features")
# print(featureList[0], "the features 1")
# print(featureList[1], "the features 2")

# print(len(featureList))

# test={}
# for v in range(0,len(featureList)):
#     tempList = featureList[v]
#     print(tempList, "this was a temp list")
#     tempdict = dict(tempList)
#     tempdict2 = dict(features = tempdict)
#     print(tempdict2, "This was another temp dict")
#     test.update(tempdict2)
#     #test = Convert(tempList)
#     #print(test, "I also did this")

# #test = dict(tempList)
# #test = Convert(featureList)

# for m in range(0, len(featureList)): ### Sort dictionary by object type
#     PointDictZip.update(featureList[m])

# print(PointDictZip, "this is the zip")


# ##print(len(featureList))      

# ##print(len(test), "I am this long")
# ##print(test, "the test worked here")


# ##for y, obj in test.items(): ### Sort dictionary by object type
#   ##  print(y, "I did this")
#    ## for z, obj in y:
#     ##   print(z)
 
#    ##  strabo_properties = sb_lines[x].get("properties")
#     ####   TraceFeatures.update(sb_lines)        
#  """
