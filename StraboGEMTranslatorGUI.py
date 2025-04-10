# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:15:57 2024

@author: ahoxey
"""

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import ttk as ttk
from PIL import ImageTk

appcwd = os.getcwd()

import StraboGEMTranslator as SGT
import StraboUtils as SU
import StraboGEMConfig as CONFIG

import StraboLineAttributeTranslators as LT
import StraboPointAttributeTranslators as PT

import StraboWorkingConfig as SWC


global input_File, file_label , input_Dest, custom_ln_symbol, custom_ln_sort, custom_ln_type, CONFIG, custom_pt_type, custom_pt_symbol, user_entry, frame_pt, Start_btn, SubmitField_btn

custom_ln_symbol = []
custom_ln_sort = []
custom_ln_type = []
custom_pt_type = [] #Orientation measurements only
custom_pt_symbol = []
user_entry_ln = []
user_entry_pt = []


input_File = ""
input_DSID = ""
input_LSID = "" 
input_OSID = "" 
input_Dest = ""


# input_File = SWC.V1
# input_DSID = SWC.V2
# input_LSID =  SWC.V3 
# input_Dest = SWC.V4


########### GUI Utility and Button Functions
def Start_Funtion():
    global input_File, input_Dest
    input_DSID = e2Var.get()
    input_LSID = e3Var.get()
    input_OSID = e4Var.get()
    
    Errors, sp_count = SGT.Translator(input_File, input_DSID, input_LSID, input_OSID, input_Dest)  
    ErrorStr = (str(sp_count) + " StraboSpot(s) processed with " + str(Errors) + " known errors")
    error_label.config(text = ErrorStr)    
    if Errors > 0:
        ErrorBTN = tk.Button(GUI, text="View Error Report", command=open_error_window)
        ErrorBTN.place(x=500, y=260)
    else: None
    
    return None

def export_error():
    global CONFIG
    import os
    folder_path = input_Dest
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'ErrorReport.txt')
    with open(file_path, 'w') as file:
        file.write("Error : SpotName" + "\n")
        for key, value in CONFIG.ErrorDict.items():
            file.write(f"{key}: {value}\n")
    return None

def open_error_window():
    global GUI
    new_window = tk.Toplevel(GUI)
    new_window.title("Error Report")
    new_window.geometry('700x500')
    
    error_canvas = tk.Canvas(new_window, width=600, height=500)
    scroll = tk.Scrollbar(new_window, command=error_canvas.yview)
    error_canvas.config(yscrollcommand=scroll.set, scrollregion=(00,00,100,3000))
    error_canvas.place(x=0, y=0)
    scroll.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
    error_frame = tk.Frame(error_canvas, width=600, height=500)
    error_canvas.create_window(0,0, anchor = tk.NW, window=error_frame)
    
    #ADD BUTTON
    tk.Button(new_window, text ='Export Report', command = lambda:export_error()).place(x=400, y=20, width=150)
    
    # Add as label
    tk.Label(error_frame, text= "Function Error", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    tk.Label(error_frame, text= "Spot Name", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 2, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    
    er_keys = list(CONFIG.ErrorDict.keys())
    for i in range(0, len(er_keys)):
        tk.Label(error_frame, text= er_keys[i], font = ("Times New Roman", 10)).grid(row = i+2, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
        tk.Label(error_frame, text= CONFIG.ErrorDict.get(er_keys[i]), font = ("Times New Roman", 10)).grid(row = i+2, column = 2, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)

    return None

def open_file():
    n_file = askopenfilename()
    global input_File, file_label
    input_File = n_file
    file_label.config(text = input_File)    
    return None
    
def dest_file():
    n_Dest = askdirectory()
    global input_Dest, dest_label
    input_Dest = n_Dest
    dest_label.config(text = input_Dest)    
    return None

def load_file():
    global custom, tab1, tab2, notebook, input_File, CONFIG
    
                          
    if not input_File :
        ErrorStr = "ERROR: Enter input file"
        error_label.config(text = ErrorStr)
        custom.set(1)
        notebook.tab(tab1, state = "disabled")
        notebook.tab(tab2, state = "disabled")
    else:
        ErrorStr = ""
        error_label.config(text = ErrorStr)
        line_types, point_types = custom_config_initation(input_File)
        notebook.tab(tab1, state = "normal")
        notebook.tab(tab2, state = "normal")
        custom_menu_build(line_types, point_types)
        notebook.select(tab1)

    return None
     
def custom_config_initation(file):
    global CONFIG
    ln_types = []
    pt_types = []
    
    # get list of linestrings
    _, _, found_lines, found_points = SU.ImportStrabo(file)
        
    # make list of line types within found_lines
    for i in range(0, len(found_lines)):
        temp_ln_types = ""
        temp_ln_types = SU.getSBLineTraceString(found_lines[i].get("properties"))
        
        ln_types.append(temp_ln_types)
                
    # omit multuples; return count?
    seen = set()
    uniq_ln_types = [x for x in ln_types if x not in seen and not seen.add(x)]
    
    # make list of orientation types within found_points
    for p in range(0, len(found_points)):
        if "orientation_data" in found_points[p].get("properties").keys():
            if not found_points[p].get("properties").get("orientation_data"):
                pass
            else:
                sb_orientation_list, _ = SU.OrientationParser(found_points[p].get("properties").get("orientation_data"))
            
                for o in range(0, len(sb_orientation_list)):
                    temp_pt_types = ""
                    temp_pt_types = SU.getSBOrientationString(sb_orientation_list[o])
                    pt_types.append(temp_pt_types)
    
    seen = set()
    uniq_pt_types = [z for z in pt_types if z not in seen and not seen.add(z)]
    
    for x in range(0, len(uniq_ln_types)):
        CONFIG.LN_SB.append(uniq_ln_types[x])
        CONFIG.LN_Gem_Sort.append(SU.SortLineFeatureClass(uniq_ln_types[x]))
        CONFIG.LN_Gem_Symbol.append(LT.getSymbol(uniq_ln_types[x]))
        CONFIG.LN_Gem_Type.append(LT.getType(uniq_ln_types[x], LT.getSymbol(uniq_ln_types[x])))
        
    for y in range(0, len(uniq_pt_types)):
        CONFIG.PT_SB.append(uniq_pt_types[y])
        CONFIG.PT_Gem_Symbol.append(PT.getOrSymbol(uniq_pt_types[y]))
        CONFIG.PT_Gem_Type.append(PT.getOrType(uniq_pt_types[y], PT.getOrSymbol(uniq_pt_types[y])))
    
    return uniq_ln_types, uniq_pt_types
    
def custom_menu_build(ln_types, pt_types):
    global CONFIG, custom_ln_sort, custom_ln_type, frame_ln, custom_pt_type, custom_pt_symbol, user_entry_ln, user_entry_pt, frame_pt
    
    # Dropdown menu options (lines)
    tk.Label(frame_ln, text= "Strabo Input", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    tk.Label(frame_ln, text= "FGDC Symbol", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 2, sticky = tk.W, padx = 2, pady = 2, columnspan = 1)
    tk.Label(frame_ln, text= "GeMS Sort", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 3, sticky = tk.W, padx = 2, pady = 2, columnspan = 1)
    tk.Label(frame_ln, text= "GeMS Line Type", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 4, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    
    for i in range(0, len(ln_types)):
        tk.Label(frame_ln, text= ln_types[i], font = ("Times New Roman", 10)).grid(row = i+1, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    
        # datatype of menu text 
        user_entry_ln.append(tk.Entry(frame_ln, width= 20))
        user_entry_ln[i].insert(0, CONFIG.LN_Gem_Symbol[i])
        user_entry_ln[i].grid(row = i+1, column = 2, sticky = tk.W, padx = 10, pady = 2, columnspan = 1)
        
        custom_ln_sort.append(tk.StringVar() )
        custom_ln_sort[i].set(CONFIG.LN_Gem_Sort[i]) 
        tk.OptionMenu(frame_ln , custom_ln_sort[i] , *CONFIG.LN_Sort_options).grid(row = i+1, column = 3, sticky = tk.W, padx = 2, pady = 2, columnspan = 1)
        
        custom_ln_type.append(tk.StringVar())
        custom_ln_type[i].set(CONFIG.LN_Gem_Type[i]) 
        tk.OptionMenu(frame_ln , custom_ln_type[i] , *CONFIG.LN_Type_options).grid(row = i+1, column = 4, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    
    # Dropdown menu options (orientation points)
    tk.Label(frame_pt, text= "Strabo Input", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    tk.Label(frame_pt, text= "FGDC Orientation Symbol", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 2 , sticky = tk.W, padx = 10, pady = 2, columnspan = 1)
    tk.Label(frame_pt, text= "GeMS Orientation Type", font = ("Times New Roman", 10), fg="blue").grid(row = 0, column = 3, sticky = tk.W, padx = 50, pady = 2, columnspan = 2)

    
    for n in range(0, len(pt_types)):
        tk.Label(frame_pt, text= pt_types[n], font = ("Times New Roman", 10)).grid(row = n+1, column = 0, sticky = tk.W, padx = 2, pady = 2, columnspan = 2)
    
        # datatype of menu text 
        # custom_pt_symbol.append(tk.StringVar())
        # custom_pt_symbol[n].set(CONFIG.PT_Gem_Symbol[n])
        # tk.Label(frame_pt, text=custom_pt_symbol[n], font = ("Times New Roman", 10)).grid(row = n+1, column = 3, sticky = tk.W, padx = 10, pady = 2, columnspan = 1)
        user_entry_pt.append(tk.Entry(frame_pt, width= 20))
        user_entry_pt[n].insert(0, CONFIG.PT_Gem_Symbol[n])
        user_entry_pt[n].grid(row = n+1, column = 2, sticky = tk.W, padx = 10, pady = 2, columnspan = 1)
        
        custom_pt_type.append(tk.StringVar())
        custom_pt_type[n].set(CONFIG.PT_Gem_Type[n]) 
        tk.OptionMenu(frame_pt , custom_pt_type[n] , *CONFIG.PT_Type_options).grid(row = n+1, column = 3, sticky = tk.W, padx = 50, pady = 2, columnspan = 1)


    return None

def set_custom():
    global CONFIG, custom_ln_sort, custom_ln_type, user_entry_ln,  custom_pt_type, user_entry_pt, Start_btn
    
    CONFIG.LN_Gem_Sort = []
    CONFIG.LN_Gem_Symbol = []
    CONFIG.LN_Gem_Type = []
    CONFIG.PT_Gem_Type = []
    CONFIG.PT_Gem_Symbol = []
    for m in range(0, len(custom_ln_sort)):
        CONFIG.LN_Gem_Sort.append(custom_ln_sort[m].get())
        CONFIG.LN_Gem_Symbol.append(user_entry_ln[m].get())
        CONFIG.LN_Gem_Type.append(custom_ln_type[m].get())
        
    for p in range(0, len(custom_pt_type)):
        CONFIG.PT_Gem_Type.append(custom_pt_type[p].get())
        CONFIG.PT_Gem_Symbol.append(user_entry_pt[p].get())
        
    return None

###################################
# Creating tkinter GUI window
GUI = tk.Tk()
#e1Var=tk.StringVar()
e2Var=tk.StringVar()
e3Var=tk.StringVar()
e4Var=tk.StringVar()
#file_label = tk.StringVar().set("File")
GUI.title("Strabo to GeMS Translator")
GUI.geometry('1200x800')

### Main Options GUI build
tk.Label(GUI, text='Step 1: Set User Variables', font = ("Times New Roman", 12), fg="green").place(x=20, y=10)

tk.Label(GUI, text='Input JSON file:', font = ("Times New Roman", 10)).place(x=20, y=40)
tk.Button(GUI, text ='Open', command = lambda:open_file()).place(x=200, y=40, width=100)
file_label = tk.Label(GUI, text="", font = ("Times New Roman", 10), bg="white", fg="blue", width=60, padx=0, wraplength=350, anchor=tk.W, justify=tk.LEFT, relief=tk.GROOVE)
file_label.place(x=20, y=80)

tk.Label(GUI, text='User Data Source ID:', font = ("Times New Roman", 10)).place(x=20, y=160)
e2 = tk.Entry(GUI, textvariable= e2Var, font = ("Times New Roman", 10)).place(x=200, y=160)

tk.Label(GUI, text='User Location Source ID:', font = ("Times New Roman", 10)).place(x=20, y=180)
e3 = tk.Entry(GUI, textvariable= e3Var, font = ("Times New Roman", 10)).place(x=200, y=180)

tk.Label(GUI, text='User Orientation Source ID:', font = ("Times New Roman", 10)).place(x=20, y=200)
e4 = tk.Entry(GUI, textvariable= e4Var, font = ("Times New Roman", 10)).place(x=200, y=200)

tk.Label(GUI, text='Output JSON file location:', font = ("Times New Roman", 10)).place(x=20, y=240)
tk.Button(GUI, text ='Set', command = lambda:dest_file()).place(x=200, y=240, width=100)
dest_label = tk.Label(GUI, text="", font = ("Times New Roman", 10), bg="white", fg="blue", width=60, padx=0, wraplength=350, anchor=tk.W, justify=tk.LEFT, relief=tk.GROOVE)
dest_label.place(x=20, y=280)

##########################################
### Custom Options GUI Tabs build
tk.Label(GUI, text='Step 2: Load File',  font = ("Times New Roman", 12), fg="green").place(x=20, y=350)
custom = tk.IntVar()
custom.set(1)
#### LoadFile Button
Load_button = tk.Button(GUI, text='Load File', width=25, command = lambda:load_file()).place(x=20, y=380)

### Old Radial buttons
#rb1 = tk.Radiobutton(GUI, text="Default (Beta)", variable=custom, value=1, command=lambda:custom_select()).place(x=20, y=360)
#rb2 = tk.Radiobutton(GUI, text="Custom", variable=custom, value=2, command=lambda:custom_select()).place(x=150, y=360)
### Radio button activates series of function that builds custom menus

tk.Label(GUI, text='Step 3: Select Attributes',  font = ("Times New Roman", 12), fg="green").place(x=20, y=420)
notebook = ttk.Notebook(GUI)
notebook.place(x=20, y=450)
#Create Tabs
tab1 = ttk.Frame(notebook, width=1100, height=200)
notebook.add(tab1, text= "Line Attributes", state = "disabled")
tab2 = ttk.Frame(notebook, width=1100, height=200)
notebook.add(tab2, text= "Orientation Attributes", state = "disabled")

## enable scrolling (Line Tab)
canvas_ln = tk.Canvas(tab1, width=900, height=200)
scroll = tk.Scrollbar(tab1, command=canvas_ln.yview)
canvas_ln.config(yscrollcommand=scroll.set, scrollregion=(00,00,100,3000)) 
canvas_ln.place(x=5, y=0)
scroll.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
frame_ln = tk.Frame(canvas_ln, width=900, height=200)
canvas_ln.create_window(0,0, anchor = tk.NW, window=frame_ln)
## enable scrolling (Point Tab)
canvas_pt = tk.Canvas(tab2, width=900, height=200)
scroll = tk.Scrollbar(tab2, command=canvas_pt.yview)
canvas_pt.config(yscrollcommand=scroll.set, scrollregion=(00,00,100,3000))
canvas_pt.place(x=5, y=0)
scroll.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
frame_pt = tk.Frame(canvas_pt, width=900, height=200)
canvas_pt.create_window(0,0, anchor = tk.NW, window=frame_pt)

# Save Fields button
tk.Label(GUI, text='Step 4: Set Attributes',  font = ("Times New Roman", 12), fg="green").place(x=20, y=690)
SubmitField_btn = tk.Button(GUI, text ='Save Custom Fields', command = lambda:set_custom()).place(x=20, y=720, width=200)



separator = ttk.Separator(GUI, orient='vertical')
separator.place(x=475, y=10, width=1, height=300)


### Logos
ImSbcanvas= tk.Canvas(GUI, width= 150, height= 150)
ImSbcanvas.place(x=490, y=10)
sb_file=appcwd + "/resources/strabo_logo.png"
sb_Image= ImageTk.PhotoImage(file=sb_file)
ImSbcanvas.create_image(0,0, anchor = tk.NW ,image=sb_Image)

ImNMBcanvas= tk.Canvas(GUI, width= 150, height= 150)
ImNMBcanvas.place(x=610, y=10)
nmb_file=appcwd + "/resources/Bureau_FullColor.png"
nmb_Image= ImageTk.PhotoImage(file=nmb_file)
ImNMBcanvas.create_image(0,0, anchor = tk.NW ,image=nmb_Image)

#### Start Button
tk.Label(GUI, text='Step 5: Start Translation',  font = ("Times New Roman", 12), fg="green").place(x=500, y=150)
Start_btn = tk.Button(GUI, text='Start Translation', width=25, command = lambda:Start_Funtion()).place(x=500, y=180)
error_label = tk.Label(GUI, text="", font = ("Times New Roman", 10), fg="red", width=60, padx=0, wraplength=360, anchor=tk.W, justify=tk.LEFT)
error_label.place(x=500, y=220)





GUI.mainloop()

