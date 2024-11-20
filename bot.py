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
def checkFoodBot(inputType, input):
    jsonFormat = """
{
    "food": <Food>,
    "serving_size": "100g",
    "macronutrient": ["Carbohydrates","Proteins","Fats","Fiber","Water"],
    "mn_amount": [],
    "mn_unit": ["g","g","g","g","g"],
    "vitamin": ["A", "C", "B1", "B2", "B3", "B6", "B12", "E", "K", "Folate"],
    "vt_amount": [],
    "vt_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
    "mineral": ["Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium", "Sodium", "Zinc", "Copper", "Manganese", "Selenium"],
    "ml_amount": [],
    "ml_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
    "calorie": <Calorie>
    "allergy": [<all potential Allergies list>]
}
    """
    if inputType == "Text":
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=f"""
            You are a professional food nutritionist. Help the user check the nutrition and potential allergies of foods per serving size of 100g.
            Please do not use any copyrighted contents. Respond ONLY with a JSON object in the following format, replacing placeholders with appropriate values:
            {jsonFormat}
            Do not include any text before or after the JSON object.
            """
        ) # **THE SYSTEM INSTRUCTION IS IMPORTANT TO GET A CORRECT JSON FORMAT!
        response = model.generate_content(f"What are the nutrition of {input}")
    elif inputType == "Image" or inputType == "Camera":
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=f"""
            You are a professional food nutritionist. Help the user to check the nutrition and potential allergies of that foods per serving size of 100g.
            Please do not use any copyrighted contents. Respond ONLY with a JSON object in the following format, replacing placeholders with appropriate values:
            {jsonFormat}
            Do not include any text before or after the JSON object.
            """
        ) # **THE SYSTEM INSTRUCTION IS IMPORTANT TO GET A CORRECT JSON FORMAT!
        response = model.generate_content(["What are the nutrition of", input])
    return(response.text)


# weightLoss.py
def weightLossSuggestionBot(age, gender, weight, height, occupation, question=None):
    # Initialize the generative model
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=f"""
        You are a professional weight loss consultant. Your task if seperated into 2 types, please do not use any copyrighted contents. If question is None, you need to ONLY calculate BMI and list suitable methods for the user to lose weight 
        based on their gender, age, current weight, current height, and occupation. Else if question is Exist, you ONLY need to answer the user's questions about the suggested methods. 
        """
    )
    
    # If it's the first interaction, provide the weight loss methods
    if question is None:
        response = model.generate_content([f"question is None: Hello, I am a {gender}, my age is {age}, my current weight is {weight}, my current height is {height}, and my occupation is {occupation}. Please suggest weight loss methods for me."])
    else:
        # If there's a follow-up question, generate a response based on it
        response = model.generate_content([f"question is Exist: A user who is a {gender}, aged {age}, with weight {weight}kg and height {height}cm, who works as a {occupation}, asked: '{question}'. Provide detailed information based on the previous suggestions you made."])

    return response.text
