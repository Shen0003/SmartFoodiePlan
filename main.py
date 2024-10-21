import streamlit as st
from streamlit_option_menu import option_menu

from page.home import home
from page.genRecipe import recipe
from page.checkRecipe import check1

# Set page configuration
st.set_page_config(page_title="Smart Foodie Planner", layout="wide")

# Custom CSS to adjust padding and font sizes
st.markdown("""
        <style>
            @media (max-width: 768px) {
                .block-container {
                    padding: 1rem 2rem 0rem 2rem;
                }
                .css-1d391kg, .css-18e3th9 {
                    font-size: 14px; /* Adjust font sizes for mobile */
                }
            }
            @media (min-width: 768px) {
                .block-container {
                    padding: 4rem 5rem 0rem 5rem;
                }
            }
        </style>
        """, unsafe_allow_html=True)

# Sidebar with options
with st.sidebar:
    menu = option_menu(
        menu_title="Main Menu",
        options=["Home", "Generate Recipe", "Check Recipe", "Cut Weight"],
        default_index=0
    )

# Main page content based on selected menu
if menu == "Home":
    home()
elif menu == "Generate Recipe":
    recipe()
elif menu == "Check Recipe":
    check1()
