'''
A minimal example using the JSON-LD context for tables and variables to reproduce the mip-cmor-tables

'''

import pyld,re,json,glob
from pyld import jsonld


# lets read the graph files. 
graphs = glob.glob('../data_descriptors/*/graph.jsonld')
data = [json.load(open(path)) for path in graphs]

table_index = graphs.index('../data_descriptors/tables/graph.jsonld')


frame = frame = {
    "@context": {
        **data[table_index]["@context"],
        
        "mip_participation":'https://wcrp-cmip.github.io/MIP_variables/data_descriptors/variables/mip-era'# rename the optional field brought in by the mip variables. (can be deleted if requiered)
    },
    # "https://wcrp-cmip.github.io/MIP_variables/data_descriptors/tables/variable_entry":{"@container":"@set"}, 
    '@type':"https://wcrp-cmip.github.io/MIP_variables/data_descriptors/tables/mip-table", # select all the tables
}

# get the frame
tables = jsonld.frame(data,frame)['@graph']

# defind our output folder
output = '../formatted/mip-tables(generated)/'


# write the files. 
for i in tables:
    with open(f'{output}/{i["id"].split("/")[-1]}','w') as f:
        
        
        if not isinstance(i['variable_entry'],list):
            i['variable_entry'] = [i['variable_entry']]
        
        i['variable_entry'] = {j['out_name']:j for j in i['variable_entry']}
    
                
        json.dump(i,f,indent=4)

