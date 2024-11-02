import streamlit as st
from bot import weightLossSuggestionBot



def cut():
    # Initialize session state for chat history and weight loss methods
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'methods' not in st.session_state:
        st.session_state.methods = ""
    with st.expander(label="Enter your body information here"):
        st.title("Body Information")
        gender = st.text_input(label="Choose Your Gender: ")
        age = st.number_input(label="Enter Your Age: ", min_value=0, step=1)
        weight = st.number_input(label="Enter Your Current Weight (kg): ", min_value=0.0, step=0.1)
        height = st.number_input(label="Enter Your Current Height (cm): ", min_value=0.0, step=0.1)
        occupation = st.text_input(label="Enter Your Occupation: ")

    if st.button("Recommend"):
        # Clear previous conversation and start a new one
        st.session_state.messages = []
        st.session_state.methods = ""

        # Get bot recommendation based on user inputs (initial suggestion)
        bot_response = weightLossSuggestionBot(gender, age, weight, height, occupation)
        st.session_state.messages.append({'role': 'assistant', 'content': bot_response})

        # Store the methods suggested by the bot for follow-up questions
        st.session_state.methods = bot_response

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User can ask questions about the weight loss methods
    if prompt := st.chat_input("Ask a question about the methods suggested"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate a response based on user's question and the methods already suggested
        if st.session_state.methods:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Call the bot to answer based on the initial methods and the user's question
                    response = weightLossSuggestionBot(gender, age, weight, height, occupation, question=prompt)
                    st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

