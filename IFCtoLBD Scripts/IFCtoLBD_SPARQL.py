# !/usr/bin/env python3
# !/usr/bin/env python3

import jpype
import os

# Enable Java imports
import jpype.imports

# Pull in types
from jpype.types import *

jpype.startJVM(classpath = ['jars/*'])

from org.linkedbuildingdata.ifc2lbd import IFCtoLBDConverter
from org.apache.jena.query import QueryFactory, QueryExecutionFactory

def process_lbd_model(lbd_folder_path, lbd_file_name):
    lbd_file_path = os.path.join(lbd_folder_path, lbd_file_name)
    
    model= QueryExecutionFactory.createDataset(lbd_file_path)
    queryString = """PREFIX bot: <https://w3id.org/bot#>

    SELECT ?building ?predicate ?object
    WHERE {
    ?building a bot:Building .
    ?building ?predicate ?object
    }"""

    query = QueryFactory.create(queryString)
    qexec = QueryExecutionFactory.create(query, model)
    results = qexec.execSelect()
    while results.hasNext() :
        soln = results.nextSolution()
        x = soln.get("building")
        print(x)

# Specify the folder containing LBD files
lbd_folder_path = "LBD files"

# Get a list of all files in the folder
lbd_files = [f for f in os.listdir(lbd_folder_path) if f.endswith(".ttl")]

# Process each LBD file in the folder
for lbd_file in lbd_files:
    process_lbd_model(lbd_folder_path, lbd_file)

jpype.shutdownJVM()

