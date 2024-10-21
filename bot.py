import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# genRecipe.py
def genRecipeBot(inputType, input):
    if inputType == "Text":
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=f"""
                You are a professional chef, help the user to generate the recipe in the format of:
                The <Food> Recipe
                Ingredients: <Ingredients>
                Instructions: <Step by step Instructions>
                Tips: <Tips>

                Enjoy your delicious <Food>!
            """
        )
        response = model.generate_content(f"What are the recipe of {input}")
    elif inputType == "Image" or inputType == "Camera":
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=f"""
                You are a professional chef, help the user to generate the recipe in the format of:
                The <Food> Recipe
                Ingredients: <Ingredients>
                Instructions: <Step by step Instructions>
                Tips: <Tips>

                Enjoy your delicious <Food>!
            """
        )
        response = model.generate_content(["What are the approximate recipe of ", input])

    st.write(response.text)

# checkRecipe.py
def checkFoodBot(input):
    jsonFormat = """
            {
                "food": <Food>,
                "serving_size": 100g,
                "nutrition": {
                    "Calories": <calorie> ,
                    "Carbohydrates": <in g>,
                    "Proteins": <in g>,
                    "Fats": <in g>,
                    "Vitamins": <all vitamins in g>,
                    "Minerals": <all minerals in g>,
                    "Water": <in g>,
                    "Fiber": <in g>
                }
            }
    """

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=f"""
        You are a professional food nutritionist. Help the user check the nutrition of foods per serving size of 100g.
        Respond ONLY with a JSON object in the following format, replacing placeholders with appropriate values:
        {jsonFormat}
        Do not include any text before or after the JSON object.
        """
    ) # **THE SYSTEM INSTRUCTION IS IMPORTANT TO GET A CORRECT JSON FORMAT!
    response = model.generate_content(f"What are the nutrition of {input}")
    return(response.text)