import streamlit as st

from components.helpers.tools import get_saved_onthologies

def uploader_tab_view():
    st.header('Отправьте свою онтологию в хранилище!')

    rdf_file = st.file_uploader("Отправьте rdf file", type=".rdf")

    if rdf_file is not None:
    # Get the filename
        filename = rdf_file.name
    
    # Save the file to disk
        with open(f"./tmp/{filename}", "wb") as file:
            file.write(rdf_file.getbuffer())

    st.divider()

    st.header("Содержимое хранилища:")

    st.table(
        {
            "Название онтологии:": get_saved_onthologies()
        }
    )


    