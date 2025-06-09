import streamlit as st
import google.generativeai as genai
import os
import json
import re

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
    "food": "<Food>",
    "serving_size": "100g",
    "macronutrient": ["Carbohydrates","Proteins","Fats","Fiber","Water"],
    "mn_amount": [0,0,0,0,0],
    "mn_unit": ["g","g","g","g","g"],
    "vitamin": ["A", "C", "B1", "B2", "B3", "B6", "B12", "E", "K", "Folate"],
    "vt_amount": [0,0,0,0,0,0,0,0,0,0],
    "vt_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
    "mineral": ["Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium", "Sodium", "Zinc", "Copper", "Manganese", "Selenium"],
    "ml_amount": [0,0,0,0,0,0,0,0,0,0],
    "ml_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
    "calorie": 0,
    "allergy": ["None"]
}
    """
    
    system_instruction = f"""
    You are a professional food nutritionist. Help the user check the nutrition and potential allergies of foods per serving size of 100g.
    
    CRITICAL: You MUST respond with ONLY a valid JSON object. No explanations, no markdown formatting, no code blocks, no additional text.
    
    Use this exact format, replacing values with actual nutritional data:
    {jsonFormat}
    
    Rules:
    - Replace all placeholder values with actual numbers
    - Use actual food name for "food" field
    - All amounts must be numbers (not strings)
    - If a nutrient is not present, use 0
    - For allergies, list actual potential allergens or ["None"] if no common allergens
    - Do not include any text before or after the JSON
    - Do not use markdown code blocks or backticks
    """
    
    try:
        if inputType == "Text":
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=system_instruction
            )
            response = model.generate_content(f"Provide nutritional information for {input}")
        elif inputType == "Image" or inputType == "Camera":
            model = genai.GenerativeModel(
                "gemini-1.5-pro",
                system_instruction=system_instruction
            )
            response = model.generate_content(["Provide nutritional information for this food", input])
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove any markdown code blocks if present
        if response_text.startswith('```'):
            response_text = re.sub(r'^```.*?\n', '', response_text)
            response_text = re.sub(r'\n```$', '', response_text)
        
        # Try to extract JSON if there's extra text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group()
        
        # Validate JSON before returning
        try:
            json.loads(response_text)
            return response_text
        except json.JSONDecodeError:
            # If still invalid, return a default structure
            st.error("API returned invalid JSON. Using default nutritional template.")
            return create_default_nutrition_json(input if inputType == "Text" else "Unknown Food")
            
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return create_default_nutrition_json(input if inputType == "Text" else "Unknown Food")

def create_default_nutrition_json(food_name):
    """Create a default nutrition JSON structure when API fails"""
    default_data = {
        "food": food_name,
        "serving_size": "100g",
        "macronutrient": ["Carbohydrates","Proteins","Fats","Fiber","Water"],
        "mn_amount": [0, 0, 0, 0, 0],
        "mn_unit": ["g","g","g","g","g"],
        "vitamin": ["A", "C", "B1", "B2", "B3", "B6", "B12", "E", "K", "Folate"],
        "vt_amount": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "vt_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
        "mineral": ["Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium", "Sodium", "Zinc", "Copper", "Manganese", "Selenium"],
        "ml_amount": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "ml_unit": ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg"],
        "calorie": 0,
        "allergy": ["Data unavailable - please consult a nutritionist"]
    }
    return json.dumps(default_data)

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