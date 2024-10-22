import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Function to convert an image to a base64 string
def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")  # Save as PNG or any other format
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def home():
    # Path to your local image
    image_path = "images/intro_banner.jpg"

    # Convert the image to a base64 string
    image_base64 = image_to_base64(image_path)

    # HTML content with inline CSS
    html_header = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        body {{
            font-family: 'Poppins', sans-serif;
            line-height: 1.6;
            color: #e0e0e0;
            margin: 0;
            padding:0;
        }}
        
        .container {{
            max-width: auto;
            margin: 0 auto;
        }}
        
        .header {{
            background-color: #1e1e1e;
            border-radius: 10px;
            margin-top: 2px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }}
        
        h1 {{
            color: #bb86fc;
            margin: 0;
            font-size: 35px;
            text-align: center;
        }}
        
        .subheader {{
            color: #03dac6;
            margin-top: 5px;
            font-size: 14px;
            text-align: center;
        }}
        
        .hero-image {{
            border-radius: 15px;
            width: 100%;
            height: auto;
        }}
    </style>

    <div class="container">
        <div class="header">
            <img src="data:image/png;base64,{image_base64}" alt="Healthy food assortment" class="hero-image">
            <h1>Welcome to Smart Foodie Planner 🍽️</h1>
            <p class="subheader">Your all-in-one solution for healthy and personalized meal planning!</p>
        </div>
    </div>
    """
    html_content = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        body {{
            font-family: 'Poppins', sans-serif;
            line-height: 1.6;
            color: #e0e0e0;
            margin: 0;
            padding:0;
        }}
        
        .container {{
            max-width: auto;
            margin: 0 auto;
        }}
        
        .section-title {{
            color: #bb86fc;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #03dac6;
            padding-bottom: 5px;
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .feature-card {{
            background-color: #2c2c2c;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }}
        
        .feature-title {{
            color: #cf6679;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .feature-description {{
            font-size: 14px;
            color: #b0b0b0;
        }}
        
        .get-started, .tip-of-the-day {{
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }}
        
        .get-started h2, .tip-of-the-day h2 {{
            color: #bb86fc;
            font-size: 18px;
            margin-top: 0;
        }}
        
        .get-started ol {{
            padding-left: 20px;
            margin-bottom: 0;
            color: #b0b0b0;
        }}
        
        .tip-of-the-day {{
            background-color: #3700b3;
            color: #e0e0e0;
        }}
        
    </style>

    <div class="container">
        <h2 class="section-title">✨ Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-title">🔍 Recipe Idea Generator</div>
                <p class="feature-description">Generate creative and delicious recipe ideas tailored to your preferences and dietary needs.</p>
            </div>
            <div class="feature-card">
                <div class="feature-title">📊 Nutritional Analysis</div>
                <p class="feature-description">Get detailed information on the 7 basic nutrition classes and calories taken for each meals.</p>
            </div>            
            <div class="feature-card">
                <div class="feature-title">🚫 Allergy Checker</div>
                <p class="feature-description">Easily check the food for potential allergens to ensure safe meal planning.</p>
            </div>
            <div class="feature-card">
                <div class="feature-title">📉 Weight Loss Suggestion</div>
                <p class="feature-description">Get suggestion of your weight loss journey with our personal assistant chatbot.</p>
            </div>
        </div>
        
        <div class="get-started">
            <h2>🚀 Get Started with the Left Sidebar Main Menu</h2>
            <ol>
                <li><strong>Generate Recipes:</strong> Click on this options to generate your recipe based on your text descriptions or images.</li>
                <li><strong>Check Nutritions and Allergies:</strong> Click on this options to ensure your meals meet the diet requirements and safe for you and your family.</li>
                <li><strong>Cut Weight:</strong> Click on this options to get your personalized recommendation of losing weight and clear your doubts using the chatbot.</li>
            </ol>
        </div>
        
        <div class="tip-of-the-day">
            <h2>💡 Tip of the Day</h2>
            <p>Incorporate colorful vegetables into your meals to ensure a wide range of nutrients and antioxidants in your diet.</p>
        </div>
    </div>
    """


    # # Display the HTML in Streamlit
    st.markdown(html_header, unsafe_allow_html=True)
    st.html(html_content)