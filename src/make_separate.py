import glob
import json
# Using p_umap from p_tqdm for parallel processing
from p_tqdm import p_umap

# Path to the directory containing JSON MIP CMOR tables
tablepath = '../formatted/mip-cmor-tables(original)/'
# Get all JSON files in the specified directory
tables = glob.glob(tablepath + '*.json')

# Utility function to return a sorted dictionary
def sd(dct):
    return {key: dct[key] for key in sorted(dct)}

# Base URL for data descriptors
# basepath = 'http://localhost:8000/data_descriptors/'
basepath = 'https://wcrp-cmip.github.io/MIP_variables/data_descriptors/'



##############################################
# Context Creation
##############################################
# Function to build a context base with optional additional values
def ctxbase(path, additional={},after={}):
    return {
        "@context": {
            "@base": f"{basepath}{path}",  # Base URL path
            "@vocab": f"{basepath}{path}",                 # Vocabulary base
            "id": "@id",                   # JSON-LD syntax for ID
            "type": "@type",               # JSON-LD syntax for type
            **additional                    # Any additional context passed
        },
        "@embed": "@always",
        # Embed the context always
        **after
    }



##############################################
# Function to write a variable JSON descriptor
##############################################
def writevar(v, t):
    # Create a unique ID for each variable in the format table_name.out_name
    nid = f'{table.lower()}.{v["out_name"].lower()}'

    # Define tables for the MIP eras (cmip6, cmip6plus)
    tables = [{"id": f'{t.lower()}.json', "mip-era": era} for era in 'cmip6 cmip6plus'.split()]

    # Update the variable dictionary by renaming 'type' to 'dtype'
    v['dtype'] = v.pop('type')

    # Prepare variable data with context and other necessary fields
    vardata = {
        "@context": f'{basepath}variables/_context',
        "id": nid + '.json',
        "type": 'mip-variable',
        "mip-tables": tables,
        "themes": ["TBC"],  # Themes to be confirmed (TBC)
        **v
    }

    # Write the variable JSON file to the data_descriptors/variables directory
    with open(f'../data_descriptors/variables/{nid}.json', 'w') as f:
        json.dump(vardata, f, indent=2)

# ##################################
# Main logic to process each MIP table

for i in tables:
    
    
    ##############################################
    # Table CTX and JSON Creation
    ##############################################
    
    # Load the MIP table JSON data
    data = json.load(open(i))

    # Set the MIP era (e.g., cmip6)
    mip = 'cmip6'

    # Sort the table header and extract the table ID
    header = sd(data['Header'])
    table = header['table_id']

    # Get the variable entries from the table
    variables = data['variable_entry']

    # Create a context for tables and write the context file
    
    table_additional = {
        "variable_entry": 
            {
                # "@reverse": f"{basepath}variables/mip-tables",
                "@context": f"{basepath}variables/_context",
          
                # "@reverse": f"{basepath}variables/mip-tables"
            }
        }
    table_after = {
        "variable_entry": 
            {
               "@container":"@set"
            },
    }
    
    # table context 
    tctx = ctxbase('tables/',table_additional)
    with open(f'../data_descriptors/tables/_context', 'w') as f:
        json.dump(tctx, f, indent=2)

    # Create table JSON with the appropriate context and metadata
    tjson = {
        '@context': f'{basepath}tables/_context',
        "id": table.lower() + '.json',
        "type": 'mip-table',
        **header
    }
    # Write the table descriptor to file
    with open(f'../data_descriptors/tables/{table.lower()}.json', 'w') as f:
        json.dump(tjson, f, indent=2)




    ##############################################
    # Variables CTX and JSON Creation
    ##############################################

    # Additional context for variables related to the tables
    variable_additional = {
    "mip-tables": 
        {
        #     "@context": f"{basepath}tables/_context",
            "@reverse": f"{basepath}tables/variable_entry"
        }
      
    }
    # variable_after = {
    # "mip-tables":
    #     {
    #         "@reverse": f"{basepath}tables/variable_entry"
    #     }
    # }
    # Create a context for variables and write the context file
    vcontext = ctxbase('variables/', variable_additional)
    with open(f'../data_descriptors/variables/_context', 'w') as f:
        json.dump(vcontext, f, indent=2)

    # Write variables in parallel (efficient for large datasets)
    p_umap(writevar, variables.values(), [table] * len(variables))





##############################################
# generate graphs 
##############################################
import os
os.system('./ld2graph.sh ../data_descriptors/tables/')
os.system('./ld2graph.sh ../data_descriptors/variables/')













    # Notes:
    # - HTML description pages should be added for each entry to enable base links to work.
    # - Reference using hash links or queries, e.g., 
    #   "ex:contains": "http://example.org/library/the-republic#introduction"
    
    # JSON-LD context snippet (optional usage example):
    # {
    #   "@context": {
    #     "nestedItem": "@nest",
    #     "listItem":  {"@id": "...", "@container": "@list"},
    #     "setItem":   {"@id": "...", "@container": "@set"},
    #     "iriItem":   {"@id": "...", "@type": "@id"},
    #     "jsonItem":  {"@id": "...", "@type": "@json"}
    #   },
    #   ...
    # }
