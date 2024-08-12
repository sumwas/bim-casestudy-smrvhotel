# Nested dictionary structure for Table 504.3
table_504_3 = {
    "A,B,E,F,M,S,U": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 75},
            "Type III": {"A": 85, "B": 75},
            "Type IV": {"HT": 85},
            "Type V": {"A": 70, "B": 60},
        },
    },
    "H-1,H-2,H-3,H-5": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
    },
    "H-4": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 75},
            "Type III": {"A": 85, "B": 75},
            "Type IV": {"HT": 85},
            "Type V": {"A": 70, "B": 60},
        },
    },
    "I-1 Condition 1,I-3": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 75},
            "Type III": {"A": 85, "B": 75},
            "Type IV": {"HT": 85},
            "Type V": {"A": 70, "B": 60},
        },
    },
    "I-1 Condition 2,I-2": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
    },
    "I-4": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 75},
            "Type III": {"A": 85, "B": 75},
            "Type IV": {"HT": 85},
            "Type V": {"A": 70, "B": 60},
        },
    },
    "R, R-1": {
        "NS": {
            "Type I": {"A": "UL", "B": 160},
            "Type II": {"A": 65, "B": 55},
            "Type III": {"A": 65, "B": 55},
            "Type IV": {"HT": 65},
            "Type V": {"A": 50, "B": 40},
        },
        "S13R": {
            "Type I": {"A": 60, "B": 60},
            "Type II": {"A": 60, "B": 60},
            "Type III": {"A": 60, "B": 60},
            "Type IV": {"HT": 60},
            "Type V": {"A": 60, "B": 60},
        },
        "S": {
            "Type I": {"A": "UL", "B": 180},
            "Type II": {"A": 85, "B": 75},
            "Type III": {"A": 85, "B": 75},
            "Type IV": {"HT": 85},
            "Type V": {"A": 70, "B": 60},
        },
    },
}


import rdflib
# Load RDF graph
rdf_graph = rdflib.Graph()
rdf_graph.parse("LBD files\smartReview\outputHotel Compliant Revit 2023 Advanced with Spaces.ifc.ttl", format="ttl")

# Getting Storey information 
with open("SPARQL\height.sparql", "r") as file:
    sparql_query = file.read()

results = rdf_graph.query(sparql_query)

# Sample height for demonstration purposes
actual_height = 57.33

# Process the results to create the BIM model and print the output
for result in results:
    construction_type = result.constructionType.toPython()
    occupancy_group = result.occupancyGroup.toPython()
    sprinkler_type = result.sprinklerType.toPython() if result.sprinklerType else "none"

    # Splitting the construction type and subtype 
    if "-" in construction_type:
        main_construction_type, subtype = construction_type.rsplit("-", 1)
    else:
        main_construction_type = construction_type
        subtype = ""

    bim_model = {
        "occupancy": occupancy_group,
        "sprinkler_system": "S" if sprinkler_type != "none" else "NS",
        "construction_type": main_construction_type.strip(),  # "Type V"
        "subtype": subtype.strip(),  # "A"
        "height": actual_height  # Example height, this should be retrieved or set appropriately
    }

    # Find the height limit for the given model
    height_limit = None
    for occupancy in table_504_3:
        if bim_model["occupancy"] in occupancy.split(", "):
            try:
                height_limit = table_504_3[occupancy][bim_model["sprinkler_system"]][bim_model["construction_type"]][bim_model["subtype"]]
            except KeyError:
                height_limit = None
            break

    # Check if the height is within the allowed limit
    if height_limit:
        if bim_model["height"] <= height_limit:
            result_message = f"The building height of {bim_model['height']} ft does not exceed the limit of {height_limit} ft as specified in Table 504.3 for:\n" \
                             f"• Occupancy - {bim_model['occupancy']},\n" \
                             f"• Construction Type - {bim_model['construction_type']},\n" \
                             f"• Subtype - {bim_model['subtype']},\n" \
                             f"• Sprinkler System - {bim_model['sprinkler_system']}."
        else:
            result_message = f"The building height of {bim_model['height']} ft exceeds the limit of {height_limit} ft as specified in Table 504.3 for:\n" \
                             f"• Occupancy - {bim_model['occupancy']},\n" \
                             f"• Construction Type - {bim_model['construction_type']},\n" \
                             f"• Subtype - {bim_model['subtype']},\n" \
                             f"• Sprinkler System - {bim_model['sprinkler_system']}."
    else:
        result_message = "Height limit not found for the given BIM model.\n" \
                         f"• Occupancy - {bim_model['occupancy']}\n" \
                         f"• Sprinkler System - {bim_model['sprinkler_system']}\n" \
                         f"• Construction Type - {bim_model['construction_type']}\n" \
                         f"• Subtype - {bim_model['subtype']}"

    print(result_message)