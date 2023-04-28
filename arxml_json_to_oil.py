import json
import os
import enum
#10.2.12
#input_file
input_f = open("application_Os_ecuc.json")
#output_file
output_f = open("output.oil", "w")

#input: the dict of CONTAINERS
#output: the oil strucutre of the CONTAINERS
def print_prefix_tabs(string, num_tabs):
    for i in range(0, num_tabs):
        print("\t", end="")
    print(string)
def recursive_parse_val(elements, num_tabs):
    #list the keys
    elements_keys = list(elements.keys())
    #print(elements_keys)
    if(elements_keys[0] == "SHORT-NAME" and elements_keys[1] == "DEFINITION-REF"):
        print_prefix_tabs(str(elements[elements_keys[1]]).split("/")[-1] + " " + str(elements[elements_keys[0]]) + " {", num_tabs)
        for i in range(2, len(elements_keys)):
            if(type(elements[elements_keys[i]]) is dict):
                recursive_parse_val(elements[elements_keys[i]], num_tabs+1)
            elif(type(elements[elements_keys[i]]) is list):
                for j in range(0, len(elements[elements_keys[i]])):
                    recursive_parse_val(elements[elements_keys[i]][j], num_tabs)
        print_prefix_tabs("}", num_tabs)
    elif("DEFINITION-REF" not in elements_keys and ("VALUE" not in elements_keys or ("VALUE-REF" not in elements_keys))):
        for i in range(0, len(elements_keys)):
            if(type(elements[elements_keys[i]]) is dict):
                recursive_parse_val(elements[elements_keys[i]], num_tabs)
            elif(type(elements[elements_keys[i]]) is list):
                for j in range(0, len(elements[elements_keys[i]])):
                    recursive_parse_val(elements[elements_keys[i]][j], num_tabs)
    else:
        if("VALUE" in elements_keys):
            print_prefix_tabs(str(elements["DEFINITION-REF"]).split("/")[-1] + " = " + str(elements["VALUE"]), num_tabs)
        elif("VALUE-REF" in elements_keys):
            print_prefix_tabs(str(elements["DEFINITION-REF"]).split("/")[-1] + " = " + str(elements["VALUE-REF"]).split("/")[-1], num_tabs)



#json objects to python dict
data = json.load(input_f)
data = data["AUTOSAR"]["AR-PACKAGES"]["AR-PACKAGE"]
data = data["ELEMENTS"]["ECUC-MODULE-CONFIGURATION-VALUES"]
data = data["CONTAINERS"]["ECUC-CONTAINER-VALUE"]

import sys
with output_f as sys.stdout:
    for elements in data:
        recursive_parse_val(elements, 0)

#close the files
input_f.close()
output_f.close()