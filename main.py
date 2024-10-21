import streamlit as st
from streamlit_option_menu import option_menu

from page.home import home
from page.genRecipe import recipe
from page.checkRecipe import check1

st.set_page_config(page_title="Smart Foodie Planner", layout="wide")
st.markdown("""
        <style>
                .block-container {
                    padding-top: 4rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

with st.sidebar:
    menu = option_menu(menu_title="Main Menu", options=["Home","Generate Recipe","Check Recipe","Cut Weight"],default_index=0)

if menu == "Home":
    home()

elif menu == "Generate Recipe":
    # st.write("GENERATE REC PAGE")
    recipe()

elif menu == "Check Recipe":
    check1()




