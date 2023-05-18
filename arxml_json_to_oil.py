import json
import os
import enum
import sys
#10.2.12
#input_file
input_f = open("application_Os_ecuc.json")
spec_f = open("spec.json")
#output_file
output_f = open("output.oil", "w")
log_f = open("log.txt", "w")

#change stdout
def change_stdout(filename_f):
    sys.stdout = filename_f
        
#input: the dict of CONTAINERS
#output: the oil strucutre of the CONTAINERS
def print_prefix_tabs(string, num_tabs):
    for i in range(0, num_tabs):
        print("\t", end="")
    print(string)

def check_spec(container, spec):
    if(container not in spec.keys()):
        sys.stdout = log_f
    else:
        sys.stdout = output_f

def recursive_parse_val(elements, num_tabs, spec, prev_container):
    #list the keys
    elements_keys = list(elements.keys())
    cur_container = ""
    if(elements_keys[0] == "SHORT-NAME" and elements_keys[1] == "DEFINITION-REF"):
        definition = str(elements["DEFINITION-REF"]).split("/")[-1]
        name = str(elements["SHORT-NAME"])
        #check spec with container
        cur_container = definition
        prev_container = cur_container
        check_spec(cur_container, spec)
        print_prefix_tabs(definition + " " + name + " {", num_tabs)
        for i in range(2, len(elements_keys)):
            if(type(elements[elements_keys[i]]) is dict):
                recursive_parse_val(elements[elements_keys[i]], num_tabs+1, spec, prev_container)
            elif(type(elements[elements_keys[i]]) is list):
                for j in range(0, len(elements[elements_keys[i]])):
                    recursive_parse_val(elements[elements_keys[i]][j], num_tabs, spec, prev_container)
        check_spec(prev_container, spec)
        print_prefix_tabs("}", num_tabs)
    elif("DEFINITION-REF" not in elements_keys and ("VALUE" not in elements_keys or ("VALUE-REF" not in elements_keys))):
        #check_spec(prev_container, cur_container, spec)
        for i in range(0, len(elements_keys)):
            if(type(elements[elements_keys[i]]) is dict):
                recursive_parse_val(elements[elements_keys[i]], num_tabs, spec, prev_container)
            elif(type(elements[elements_keys[i]]) is list):
                for j in range(0, len(elements[elements_keys[i]])):
                    recursive_parse_val(elements[elements_keys[i]][j], num_tabs, spec, prev_container)
    else:
        #check spec with parent container
        if("VALUE" in elements_keys):
            definition = str(elements["DEFINITION-REF"]).split("/")[-1]
            value = str(elements["VALUE"])
            
            check_spec(prev_container, spec)
                
            if(type(elements["VALUE"]) is str):
                print_prefix_tabs(definition + " = " + "\"" + value + "\"", num_tabs)
            else:
                print_prefix_tabs(definition + " = " + value, num_tabs)
                
        elif("VALUE-REF" in elements_keys): 
            definition = str(elements["DEFINITION-REF"]).split("/")[-1]
            value = str(elements["VALUE-REF"])
            
            check_spec(prev_container, spec)

            if(type(elements["VALUE-REF"]) is str):
                print_prefix_tabs(definition + " = " + "\"" + value + "\"", num_tabs)
            else:
                print_prefix_tabs(definition + " = " + value, num_tabs)



#json objects to python dict
data = json.load(input_f)
data = data["AUTOSAR"]["AR-PACKAGES"]["AR-PACKAGE"]
data = data["ELEMENTS"]["ECUC-MODULE-CONFIGURATION-VALUES"]
data = data["CONTAINERS"]["ECUC-CONTAINER-VALUE"]
spec = json.load(spec_f)
spec = spec["SPEC-CONFIGURATION"]["SPEC-CONTAINERS"]


with output_f as sys.stdout:
    prev_container = ""
    for elements in data:
        recursive_parse_val(elements, 0, spec, prev_container)
#close the files
input_f.close()
output_f.close()