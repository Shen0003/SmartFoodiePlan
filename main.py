import streamlit as st
from streamlit_option_menu import option_menu

from page.home import home
from page.genRecipe import recipe
from page.checkNutrition import check
from page.weightLoss import cut

# Set page configuration
st.set_page_config(page_title="Stupid Foodie Planner", layout="wide")

# Custom CSS to adjust padding and font sizes
st.markdown("""
        <style>
            @media (max-width: 768px) {
                .block-container {
                    padding: 4rem 2rem 0rem 2rem;
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
        options=["Home", "Generate Recipe", "Check Nutrition and Allergies", "Cut Weight"],
        default_index=0
    )
    inputType = st.radio("Choose your input type: ",["Text","Image","Camera"])


# Main page content based on selected menu
if menu == "Home":
    home()
elif menu == "Generate Recipe":
    recipe(inputType)
elif menu == "Check Nutrition and Allergies":
    check(inputType)
elif menu == "Cut Weight":
    cut()
