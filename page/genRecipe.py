import streamlit as st
import PIL.Image
from io import BytesIO

from bot import genRecipeBot

def recipe(inputType):
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
    if st.button(label="Generate"):
        if user_input is not None:
            st.divider()
            try:
                if inputType == "Text":
                    with st.spinner("Analyzing food and generating recipe..."):
                        genRecipeBot(inputType=inputType, input=user_input)

                elif inputType == "Image":
                    # Open the uploaded image
                    image = PIL.Image.open(user_input)
                    st.image(image, caption='Uploaded Image', use_column_width=True)
                    
                    with st.spinner("Analyzing image and generating recipe..."):
                        genRecipeBot(inputType=inputType, input=image)

                elif inputType == "Camera":
                    # Save the camera input to a file-like object and treat it as an uploaded file
                    image = PIL.Image.open(BytesIO(user_input.getvalue()))  # Convert to an image object
                    st.image(image, caption='Captured Image', use_column_width=True)
                    
                    with st.spinner("Analyzing captured image and generating recipe..."):
                        genRecipeBot(inputType="Image", input=image)  # Treat the camera capture as an uploaded image
                        
            except Exception as e:
                st.error(f"An error occurred while generating the recipe: {str(e)}")
                st.error("Please try again or contact support if the problem persists.")
        else:
            st.warning("Please provide input before clicking Generate.")