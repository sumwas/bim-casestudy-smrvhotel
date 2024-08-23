from SPARQLWrapper import SPARQLWrapper, JSON
import json
import pandas as pd
import rdflib
from rdflib import Namespace
import os

# Load your RDF data from a TTL file with the specified file path
rdf_graph = rdflib.Graph()
rdf_graph.parse("LBD files/output_Duplex_A_20110505.ifc.ttl", format="turtle")

# Define the namespaces used in your query
ns1 = Namespace("http://lbd.arch.rwth-aachen.de/props#")
ns2 = Namespace("https://w3id.org/bot#")
owl = Namespace("http://www.w3.org/2002/07/owl#")

# SPARQL query
query = """
PREFIX ns1: <http://lbd.arch.rwth-aachen.de/props#>
PREFIX ns2: <https://w3id.org/bot#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?zoneName ?storeyName ?spaceName ?elementName
WHERE {
  ?zone ns2:hasBuilding/ns2:hasStorey/ns2:hasSpace/ns2:containsElement ?element .
  ?zone ns1:nameIfcRoot_attribute_simple ?zoneName .
  ?element ns1:nameIfcRoot_attribute_simple ?elementName .
  ?zone ns2:hasBuilding/ns2:hasStorey/ns2:hasSpace/ns1:nameIfcRoot_attribute_simple ?spaceName .
  ?zone ns2:hasBuilding/ns2:hasStorey/ns1:nameIfcRoot_attribute_simple ?storeyName .
}


"""

# Execute the SPARQL query on the RDF graph
results = rdf_graph.query(query)

# Process and print the results
for row in results:
    # You can access specific variables in the query using row["variable_name"]
    # For example, row["wall"] will give you the value of ?wall in each result
    print(row)
    
# Convert query results to a list of dictionaries
results_list = [dict(row.asdict()) for row in results]

output_directory = "JSON files"

json_file_path = os.path.join(output_directory, "HierarchySimple.json")

# Save results as a JSON file
with open(json_file_path, "w") as json_file:
    json.dump(results_list, json_file, indent=4)

print(f"Query results saved as {json_file_path}")

