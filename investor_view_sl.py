# This is a Python script that uses the Streamlit library to create an interactive web application. 
# The purpose of this web application is to simulate a conversation between an entrepreneur and an investor. 
# The conversation is facilitated by GPT-3.5-turbo, a powerful language model from OpenAI. Here is a breakdown of the code:
# Note: This script requires an OpenAI API key to function correctly and the user needs to supply it through the Streamlit interface. This key provides access to the OpenAI GPT-3.5-turbo API used for generating responses.








# Importing libraries: Importing necessary libraries for the application including Streamlit (st), pandas (pd), and OpenAI.
import streamlit as st
import pandas as pd
from openai.error import OpenAIError
import openai

# This function sets the OpenAI API key in the Streamlit session state. The API key is necessary for making requests to the OpenAI GPT-3.5-turbo API.
def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["api_key_configured"] = True

# This function is used to reset the 'submit' state in the Streamlit session state.    
def clear_submit():
    st.session_state["submit"] = False

# This function creates a sidebar for the web application where the user can enter the OpenAI API key and view information about the application.
def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. write in your own words the startup idea\n"
            "3. presss submit botton\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "investorView is an app that simulate conversation between entrepreneur and investor.\n" 
            "draft your idea in your own words and see how chatgpt takes it to the next level and answers the hardest questions an investor can ask\n"
        )
        st.markdown("---")


        

# Main script: In the main part of the script, it sets the page title, icon, and layout for the Streamlit web application, sets a header, calls the sidebar() function, and provides a text area for the user to write their startup idea. It then handles the interaction when a user clicks the "Submit" button. It first checks if the API key is configured and if an idea has been entered. If both conditions are met, it initiates a conversation with the OpenAI model.

st.set_page_config(page_title="InvestorView", page_icon="♜", layout="wide")
st.header("♜InvestorView")
sidebar()        
st.write("Write about your startup. be specific as you can. include the problem, solution, stage (ideation, prototype, design parnters, paying costumers, profits), technologies, market, what are you looking for")
query = st.text_area("draft it here ", on_change=clear_submit)
Max_Iter = 5       
button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not query:
        st.error("Please enter your idea!")
    else:
        st.session_state["submit"] = True
        
        try:
            # OpenAI model interaction: The conversation involves back-and-forth interactions with the GPT-3.5-turbo model. 
            # The model is presented as an investor responding to the startup pitch provided by the user. 
            # The conversation iterates up to Max_Iter times (defined as 5 in this case), simulating a rich conversation. The progress of the conversation is also displayed using a progress bar.
            openai.api_key = st.session_state.get("OPENAI_API_KEY")
            bar = st.progress(0)
            ent_sys = f'you are Nir, an enrepreneur that present to an investor your startup: {query}'
            investor_sys = '''you are investor that listen to a pitch and respond. be very precise. ask as many question as you wish. cover all aspects.  
                              make sure you cover: problem, solution, who are the buyer, who are the user, go to market strategy, pricing model, competitors, technology aspects, financials, etc.
                              make sure enrepreneur answer all your question and ask again if the answer is not full.'''
            ent_msgs = [
                        {"role": "system", "content": ent_sys},
                        {"role": "user", "content": "start the pitch"},
                       ]
            investor_msgs = [
                        {"role": "system", "content": investor_sys},
                       ]

            for i in range(Max_Iter):
                st.markdown("\n######### enrepreneur #########\n")
                ent_res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=ent_msgs,
                    stream=True)
                ent_res_text = ""
                text_placeholder = st.empty()
                text_placeholder.markdown("{}".format(ent_res_text))
                for chunk in ent_res:
                    chunk_message = chunk['choices'][0]['delta']  # extract the message
                    if "content" in chunk_message:
                        message_text = chunk_message['content']
                        ent_res_text += message_text
                        text_placeholder.markdown("{}".format(ent_res_text))
                ent_msgs.append({"role": "assistant", "content": ent_res_text}) # ent_res['choices'][-1].message["content"]
                investor_msgs.append({"role": "user", "content": ent_res_text})
                bar.progress(round((2*(i+1)-1)/Max_Iter/2*100))
                
                st.markdown("\n#########  investor: #########\n")
                investor_res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=investor_msgs,
                    stream=True)
                investor_res_text = ""
                text_placeholder = st.empty()
                text_placeholder.markdown("{}".format(investor_res_text))    
                for chunk in investor_res:
                    chunk_message = chunk['choices'][0]['delta']  # extract the message
                    if "content" in chunk_message:
                        message_text = chunk_message['content']
                        investor_res_text += message_text
                        text_placeholder.markdown("{}".format(investor_res_text))
                investor_msgs.append({"role": "assistant", "content": investor_res_text})
                ent_msgs.append({"role": "user", "content": investor_res_text})
                bar.progress(round((2*(i+1))/Max_Iter/2*100))
     
            

        except OpenAIError as e:
            # Error handling: Errors during the interaction with the OpenAI model are caught and displayed to the user.
            st.error(e._message)
        
            