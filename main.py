import streamlit as st

from components.helpers.tools import get_saved_onthologies
from components.tabs.show import show_tab_view
from components.tabs.uploader import uploader_tab_view
from components.tabs.create import create_view_tab

def main():
    st.title("RDF менеджер by Slavyan")

    tab1, tab2 = st.tabs(["Просмотр и управление", "Сохранение"])

    with tab1:
        show_tab_view()
    with tab2:
        uploader_tab_view()

if __name__ == "__main__":
    main()