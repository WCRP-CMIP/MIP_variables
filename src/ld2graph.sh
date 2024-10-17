#!/bin/bash

# Set the target directory
DIR="$1"

# Initialize an empty JSON-LD array structure

echo '{"@context": ' > "$DIR/graph.jsonld"
context=$(jq '.["@context"]' "$DIR/_context") 
echo "$context," >> "$DIR/graph.jsonld"


echo '"@graph": [' >> "$DIR/graph.jsonld"

# Loop through all jsonld files in the directory
for file in "$DIR"/*.json; do
    # Read the content of each file and strip off the enclosing braces
    # content=$(sed '1d;$d' "$file")
    # read the file
    content=$(cat "$file") 
    
    # Append the content of the file to the graph.jsonld file
    echo "$content," >> "$DIR/graph.jsonld"
done

# Remove the last comma (to maintain valid JSON format)
# mac and linux have different sed inplace cmds 
# sed -i '$ s/,$//' "$DIR/graph.jsonld"
sed '$ s/,$//' "$DIR/graph.jsonld" > "$DIR/temp_graph.jsonld" && mv "$DIR/temp_graph.jsonld" "$DIR/graph.jsonld"



# Close the JSON-LD structure
echo ']}' >> "$DIR/graph.jsonld"

echo "Combined JSON-LD file created at $DIR/graph.jsonld"

