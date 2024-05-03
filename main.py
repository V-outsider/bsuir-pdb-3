import streamlit as st

from components.tabs.show import show_tab_view
from components.tabs.uploader import uploader_tab_view

def main():
    st.title("3 лабка онтологии менеджерить Гаевой")

    tab1, tab2 = st.tabs(["Просмотр и управление", "Сохранение"])

    with tab1:
        show_tab_view()
    with tab2:
        uploader_tab_view()

if __name__ == "__main__":
    main()