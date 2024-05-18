import random
import networkx as nx
import pandas as pd
import streamlit as st
import datetime
import asyncio

from rdflib import Graph, URIRef, RDF, OWL, RDFS
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
        with open(f'./tmp/{option}', 'r', encoding='utf-8') as rdf_file:
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
    
    class_name = st.text_input("Введите имя класса:")

    if st.button("Создать класс отдельно"):

        class_uri = f"http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#{class_name}"

        g.add((URIRef(class_uri), RDF.type, OWL.Class))

    
        # Сериализуйте граф в формате XML и сохраните его
        g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
    
        st.write("Класс создан.")

    object_name = st.text_input("Введите имя объекта:")

    # object_name = st.text_input("Введите имя объекта:")
    # instance_name = st.text_input("Введите имя экземпляра:")
    if st.button("Создать обьект отдельно"):
    # Генерируйте соответствующие тройки RDF на основе введенных значений в поля
        
        object_uri = f"http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#{object_name}"

        g.add((URIRef(object_uri), RDF.type, OWL.ObjectProperty))

        g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
    
        st.write("Обьект создан.")

    instance_name = st.text_input("Введите имя экземпляра:")
    if st.button("Создать экземпляр отдельно"):

        instance_uri = f"http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#{instance_name}"

        g.add((URIRef(instance_uri), RDF.type, OWL.NamedIndividual))
    
        g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
    
        st.write("Экземпляр создан.")

    
# Получить список классов из графа
    class_names = [str(class_uri).split('#')[-1] for class_uri in g.subjects(RDF.type, OWL.Class)]
    
    # Вывести выпадающий список для выбора класса
    selected_class = st.selectbox("Выберите класс", class_names)

    if st.button("Создать"):
        instance_name = st.text_input("Введите имя нового экземпляра")
    
        if instance_name:
            # Получить URI выбранного класса
            class_uri = next(g.subjects(RDF.type, URIRef(selected_class)))
    
            print(class_uri)


            print(class_uri)

            # Генерируйте URI для нового экземпляра
            instance_uri = f"{class_uri}#{instance_name}"
    
            # Добавить новый экземпляр в выбранный класс
            g.add((URIRef(instance_uri), RDF.type, URIRef(class_uri)))
    
            # Сериализуйте граф в формате XML и сохраните его
            g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
    
            st.write("Экземпляр успешно создан в классе", selected_class)
        else:
            st.write("Введите имя нового экземпляра.")
    
        if st.button("Сохранить"):
            # Сериализуйте граф в формате XML и сохраните его
            g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
    
        st.write("Изменения сохранены.")
    
# Получить список всех классов
    class_names = [str(class_uri).split('#')[-1] for class_uri in g.subjects(RDF.type, OWL.Class)]

    # Вывести выпадающий список для выбора класса
    selected_class = st.selectbox("Выберите классв", class_names)

    selected_instance = st.text_input("Введите имя 'dddddd:")
    # Получить URI выбранного класса
    # class_uri = next(g.subjects(RDF.type, URIRef(selected_class)))
    class_uri = f"http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#{selected_class}"
    # Получить список всех экземпляров выбранного класса
        # Вывести выпадающий список для выбора экземпляра
    
    if st.button("Связать"):
        # Получить URI выбранного экземпляра
        # Определить URI выбранного экземпляра
        instance_uri = f"http://www.semanticweb.org/eyon/ontologies/2024/3/untitled-ontology-14#{selected_instance}"
        # Добавить тройку с связью между классом и экземпляром
        g.add((URIRef(instance_uri), RDF.type, URIRef(class_uri)))
        
        # Сериализовать граф в формате XML и сохранить его
        g.serialize(destination="tmp/modified_data2_.rdf", format="xml")
        st.write("Связь успешно создана.")