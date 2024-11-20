import streamlit as st
import json
import pandas as pd
# import matplotlib.pyplot as plt
import altair as alt
import PIL
from io import BytesIO

from bot import checkFoodBot

def graph(json_input):
    # Data preparation
    foodInfo = json.loads(json_input)
    st.write(foodInfo) ## For debugging purposes

    macro_data = pd.DataFrame({
        'Nutrient': foodInfo['macronutrient'],
        'Amount': foodInfo['mn_amount'],
        'Unit': foodInfo['mn_unit']
    })

    vitamins_data = pd.DataFrame({
        'Vitamin': foodInfo['vitamin'],
        'Amount': foodInfo['vt_amount'],
        'Unit': foodInfo['vt_unit']
    })

    minerals_data = pd.DataFrame({
        'Mineral': foodInfo['mineral'],
        'Amount': foodInfo['ml_amount'],
        'Unit': foodInfo['ml_unit']
    })

    # Streamlit app
    st.divider()
    st.title(f"{foodInfo['food']} Nutritional Information (per 100g)")

    # 1. Calories Taken
    st.write('### 1. Calories: ',str(foodInfo['calorie']),'cal')

    st.subheader("2. Potential Allergies")
    df = pd.DataFrame({"Allergies Types:": foodInfo['allergy']})
    df.index = range(1, len(df)+1)
    st.write(df)

    # 2. Horizontal bar chart for macronutrients
    st.subheader("3. Macronutrients")
    macro_chart = alt.Chart(macro_data).mark_bar().encode(
        y=alt.Y('Nutrient:N', sort='-x'),
        x=alt.X('Amount:Q'),
        tooltip=['Nutrient', 'Amount', 'Unit']
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(macro_chart)

    # 3. Lollipop chart for vitamins
    st.subheader("4. Vitamins")
    vitamins_chart = alt.Chart(vitamins_data).mark_bar().encode(
        y=alt.Y('Vitamin:N', sort='-x'),
        x=alt.X('Amount:Q'),
        tooltip=['Vitamin', 'Amount', 'Unit']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(vitamins_chart)

    # 4. Bar chart for minerals
    st.subheader("5. Minerals")
    minerals_chart = alt.Chart(minerals_data).mark_bar().encode(
        y=alt.Y('Mineral:N', sort='-x'),
        x=alt.X('Amount:Q'),
        tooltip=['Mineral', 'Amount', 'Unit']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(minerals_chart)

def check(inputType):
    # st.markdown("<h1 style='text-align: center; margin-bottom: 0px; padding-bottom: 0px;'>Select Input Types</h1>", unsafe_allow_html=True)

    # # Create a layout with columns for centering the content
    # col1, col2, col3 = st.columns([2.3, 2, 1])  # The center column is wider
    # with col2:
    #     inputType = st.radio("", options=["Text", "Image", "Camera"], index=0)
    ################################################################################
    # Initialize a variable to store the input
    user_input = None

    if inputType == "Text":
        user_input = st.text_input(label="Describe the food:")
    elif inputType == "Image":
        user_input = st.file_uploader(label="Upload an image of the food:", type=["png", "jpg", "jpeg"])
    elif inputType == "Camera":
        user_input = st.camera_input(label="Take a picture of the food:")

    # Create a submit button
    if st.button(label="Check"):
        if user_input is not None:
            if inputType == "Text":
                json_input = checkFoodBot(inputType=inputType, input=user_input)
                graph(json_input)

            elif inputType == "Image":
                # Open the uploaded image
                image = PIL.Image.open(user_input)
                st.image(image, caption='Uploaded Image', use_column_width=True)
                json_input = checkFoodBot(inputType=inputType, input=image)
                graph(json_input)

            elif inputType == "Camera":
                # Save the camera input to a file-like object and treat it as an uploaded file
                image = PIL.Image.open(BytesIO(user_input.getvalue()))  # Convert to an image object
                st.image(image, caption='Captured Image', use_column_width=True)
                json_input = checkFoodBot(inputType="Image", input=image) # Treat the camera capture as an uploaded image
                graph(json_input)
        else:
            st.write("No input provided.")
    




