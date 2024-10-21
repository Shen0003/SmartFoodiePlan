import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

from bot import checkFoodBot

def check1():
    # data = {'Carbohydrates': 5, 'Proteins': 10, 'Fats': 20, 'Vitamins': 35, 'Minerals': 10, 'Fibre': 10, 'Water': 10}
    
    # plt.figure(figsize=(10, 6))  # Optional: set the size of the figure
    # plt.barh(list(data.keys()), list(data.values()))
    # plt.xlabel('Nutritional Values')  # Optional: add labels to axes
    # plt.title('Nutritional Content of the Recipe (per 100g)')  # Optional: add a title

    # st.pyplot(plt)  # Display the figure in Streamlit
    # plt.clf()  # Clear the current figure to prevent overlap in subsequent calls
    foodInfo = json.loads(checkFoodBot("fried rice"))
    st.write(foodInfo)


