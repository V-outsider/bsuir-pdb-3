import networkx as nx
import pandas as pd
import streamlit as st
import datetime
import asyncio

from rdflib import Graph
from streamlit_agraph import agraph, Node, Edge, Config

from components.helpers.tools import get_saved_onthologies

def filter_nodes(x):
    parts = x.split("#")
    return parts[1] if len(parts) > 1 else parts[0]

def execute_sparql(g, query):
    results = []
    try:
        query_result = g.query(query)
        for row in query_result:
            results.append(row)
    except Exception as e:
        results.append(("Error:", str(e)))
    return results

def show_tab_view():
    g = Graph()

    option = st.selectbox(
    'Выберите существующую онтологию!',
    get_saved_onthologies())

    st.divider()

    if option:
        with open(f'./tmp/{option}', 'r') as rdf_file:
            if rdf_file is not None:
                edges = []
                nodes = []
                
                g.parse(rdf_file, format="xml")

                # Create a NetworkX graph from the RDF data
                nx_graph = nx.Graph()
                for subject, predicate, obj in g:
                    sub_cleared = filter_nodes(subject)
                    pred_cleared = filter_nodes(predicate)
                    obj_cleared = filter_nodes(obj)

                    # print(sub_cleared, pred_cleared, obj_cleared)
                    nodes.append(Node(id=sub_cleared, label=sub_cleared, color="#FFA500"))
                    nodes.append(Node(id=obj_cleared, label=obj_cleared, color="#FFA500"))
                    edges.append(Edge(
                        source=sub_cleared, 
                        label=pred_cleared, 
                        target=obj_cleared
                    ))

                nodes_ = [(x.id, x) for x in nodes]
                nodes_unique = []
                
                for x in range(len(nodes_)-1):
                    if nodes_[x][1].id not in [n[0] for n in nodes_unique]:
                        nodes_unique.append(nodes_[x])


                config = Config(
                    # hierarchical=True,
                    width=1500, 
                    height=300, 
                    directed=True,
                    nodeHighlightBehavior=True, 
                    highlightColor="#F7A7A6",
                    collapsible=True,
                    node={'labelProperty':'label'},
                    link={'labelProperty': 'label', 'renderLabel': True}
                    ) 

                return_value = agraph(nodes=[x[1] for x in nodes_unique], 
                            edges=edges, 
                            config=config)
                
    st.divider()
    st.header('Консоль запросов SPARQL (SELECT)')


    sparql_req = st.text_area(
        "Введите SPARQL запрос:",
        '''SELECT ?subject ?object WHERE { ?subject rdfs:subClassOf ?object } LIMIT 5'''
    )

    if st.button("Execute select"):
        results = execute_sparql(g, sparql_req)

        # Display the results
        if results:
            print(results)
            st.write("Результат выполнения запроса:")
            new_dict = {}
            for result in list(map(lambda x: x.asdict(), results)):
                for key, value in result.items():
                    new_dict.setdefault(key, []).append(value)
            
            st.table(new_dict)
        else:
            st.write("No results found.")

    st.divider()
    st.header('Консоль запросов SPARQL (UPDATE)')

    sparql_update_req = st.text_area(
        "Введите SPARQL (INSERT/UPDATE/DELETE) запрос:",
        '''PREFIX ex: <http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#>

           INSERT DATA {
            ex:John ex:age 30 ;
            ex:name "John Doe" .
            ex:Mary ex:age 25 ;
            ex:name "Mary Smith" .
}
        '''
    )

    if st.button("Execute update"):
        g.update(sparql_update_req)

        g.serialize(destination=f"./tmp/{option}_modified_data_{datetime.datetime.now()}.rdf", format="xml")

        st.write("Result - Success: 200 OK")
