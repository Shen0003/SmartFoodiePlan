import streamlit as st
import json
import pandas as pd
import altair as alt
import PIL
from io import BytesIO

from bot import checkFoodBot

def graph(json_input):
    try:
        # Data preparation
        foodInfo = json.loads(json_input)
        # st.write("Debug - Raw API Response:", foodInfo) ## For debugging purposes

        # Validate required fields
        required_fields = ['food', 'calorie', 'allergy', 'macronutrient', 'mn_amount', 
                          'mn_unit', 'vitamin', 'vt_amount', 'vt_unit', 'mineral', 
                          'ml_amount', 'ml_unit']
        
        for field in required_fields:
            if field not in foodInfo:
                st.error(f"Missing required field: {field}")
                return

        # Ensure arrays have the same length
        macro_data = pd.DataFrame({
            'Nutrient': foodInfo['macronutrient'],
            'Amount': foodInfo['mn_amount'][:len(foodInfo['macronutrient'])],
            'Unit': foodInfo['mn_unit'][:len(foodInfo['macronutrient'])]
        })

        vitamins_data = pd.DataFrame({
            'Vitamin': foodInfo['vitamin'],
            'Amount': foodInfo['vt_amount'][:len(foodInfo['vitamin'])],
            'Unit': foodInfo['vt_unit'][:len(foodInfo['vitamin'])]
        })

        minerals_data = pd.DataFrame({
            'Mineral': foodInfo['mineral'],
            'Amount': foodInfo['ml_amount'][:len(foodInfo['mineral'])],
            'Unit': foodInfo['ml_unit'][:len(foodInfo['mineral'])]
        })

        # Streamlit app
        st.divider()
        st.title(f"{foodInfo['food']} Nutritional Information (per 100g)")

        # 1. Calories Taken
        st.write('### 1. Calories: ', str(foodInfo['calorie']), ' cal')

        # 2. Allergies
        st.subheader("2. Potential Allergies")
        if foodInfo['allergy'] and len(foodInfo['allergy']) > 0:
            df = pd.DataFrame({"Allergies Types:": foodInfo['allergy']})
            df.index = range(1, len(df)+1)
            st.write(df)
        else:
            st.write("No common allergens identified")

        # 3. Horizontal bar chart for macronutrients
        st.subheader("3. Macronutrients")
        if not macro_data.empty and macro_data['Amount'].sum() > 0:
            macro_chart = alt.Chart(macro_data).mark_bar().encode(
                y=alt.Y('Nutrient:N', sort='-x'),
                x=alt.X('Amount:Q'),
                tooltip=['Nutrient', 'Amount', 'Unit']
            ).properties(
                width=600,
                height=300
            )
            st.altair_chart(macro_chart)
        else:
            st.write("Macronutrient data not available")

        # 4. Lollipop chart for vitamins
        st.subheader("4. Vitamins")
        if not vitamins_data.empty and vitamins_data['Amount'].sum() > 0:
            vitamins_chart = alt.Chart(vitamins_data).mark_bar().encode(
                y=alt.Y('Vitamin:N', sort='-x'),
                x=alt.X('Amount:Q'),
                tooltip=['Vitamin', 'Amount', 'Unit']
            ).properties(
                width=600,
                height=400
            )
            st.altair_chart(vitamins_chart)
        else:
            st.write("Vitamin data not available")

        # 5. Bar chart for minerals
        st.subheader("5. Minerals")
        if not minerals_data.empty and minerals_data['Amount'].sum() > 0:
            minerals_chart = alt.Chart(minerals_data).mark_bar().encode(
                y=alt.Y('Mineral:N', sort='-x'),
                x=alt.X('Amount:Q'),
                tooltip=['Mineral', 'Amount', 'Unit']
            ).properties(
                width=600,
                height=400
            )
            st.altair_chart(minerals_chart)
        else:
            st.write("Mineral data not available")

    except json.JSONDecodeError as e:
        st.error("Error: The API returned invalid JSON data. Please try again.")
        st.error(f"JSON Error Details: {str(e)}")
        st.text("Raw Response:")
        st.text(json_input[:500] + "..." if len(json_input) > 500 else json_input)
        
    except KeyError as e:
        st.error(f"Error: Missing expected data field: {str(e)}")
        st.text("Available fields:")
        try:
            foodInfo = json.loads(json_input)
            st.text(list(foodInfo.keys()))
        except:
            st.text("Unable to parse response")
            
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.text("Raw Response:")
        st.text(json_input[:500] + "..." if len(json_input) > 500 else json_input)

def check(inputType):
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
            try:
                if inputType == "Text":
                    with st.spinner("Analyzing nutrition and Finding possible allergen..."):
                        json_input = checkFoodBot(inputType=inputType, input=user_input)
                        if json_input:
                            graph(json_input)
                        else:
                            st.error("Failed to get nutritional data. Please try again.")

                elif inputType == "Image":
                    # Open the uploaded image
                    image = PIL.Image.open(user_input)
                    st.image(image, caption='Uploaded Image', use_column_width=True)
                    
                    with st.spinner("Analyzing nutrition from image..."):
                        json_input = checkFoodBot(inputType=inputType, input=image)
                        if json_input:
                            graph(json_input)
                        else:
                            st.error("Failed to get nutritional data. Please try again.")

                elif inputType == "Camera":
                    # Save the camera input to a file-like object and treat it as an uploaded file
                    image = PIL.Image.open(BytesIO(user_input.getvalue()))
                    st.image(image, caption='Captured Image', use_column_width=True)
                    
                    with st.spinner("Analyzing nutrition from camera image..."):
                        json_input = checkFoodBot(inputType="Image", input=image)
                        if json_input:
                            graph(json_input)
                        else:
                            st.error("Failed to get nutritional data. Please try again.")
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please try again or contact support if the problem persists.")
        else:
            st.warning("Please provide input before clicking Check.")