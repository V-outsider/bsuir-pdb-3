import datetime
import streamlit as st
from rdflib import RDF, RDFS, Graph


from components.helpers.tools import get_saved_onthologies

def get_classes_from_ontology(graph):
    classes = set()
    for subject, predicate, obj in graph:
        if predicate == RDF.type and obj != RDFS.Resource:
            classes.add(obj.split("#")[-1])
    return list(classes)

def create_view_tab(selected_onto):
    g = Graph()

    st.title("Ontology Object Creation Form")


    st.write(get_saved_onthologies())
    if selected_onto:
        with open(f'./tmp/{selected_onto}', 'r') as rdf_file:
            if rdf_file is not None:
                g.parse(rdf_file, format="xml")

    
    # Object selectors
                # MultiLocatedSelectbox(
                #     options=("Option 1", "Option 2", "Option 3"),
                #     key="option"
                # )
                selected_class = st.selectbox("Select Class", get_classes_from_ontology(g))
                print(get_classes_from_ontology(g))
    
    # Object properties
                # object_property_value = st.text_input("Object Property Value")
    
    # Submit button
    # if st.button("Create Object"):
    #     # Generate a new URI for the object
    #     new_object_uri = ontology_namespace["Object_" + str(len(graph) + 1)]
        
    #     # Add the object to the graph
    #     graph.add((new_object_uri, RDF.type, ontology_namespace[selected_class]))
    #     graph.add((new_object_uri, ontology_namespace["objectProperty"], Literal(object_property_value)))
        
    #     # Save the changes to the ontology file
    #     g.serialize(destination=f"./tmp/{selected_onthology}_modified_data_{datetime.datetime.now()}.rdf", format="xml")
        
    #     st.success("Object created successfully!")