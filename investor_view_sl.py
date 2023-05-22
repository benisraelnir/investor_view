import streamlit as st
import pandas as pd
from openai.error import OpenAIError
import openai

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["api_key_configured"] = True

    
def clear_submit():
    st.session_state["submit"] = False

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


        



st.set_page_config(page_title="InvestorView", page_icon="♜", layout="wide")
st.header("♜InvestorView")

sidebar()        
st.write("Write about your startup. be specific as you can. include the problem, solution, stage (ideation, prototype, design parnters, paying costumers, profits), technologies, market, what are you looking for")
query = st.text_area("draft it here ", on_change=clear_submit)
       
button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not query:
        st.error("Please enter your idea!")
    else:
        st.session_state["submit"] = True
        
        try:
            
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

            for i in range(5):
                ent_res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages= ent_msgs)
                ent_msgs.append({"role": "assistant", "content": ent_res['choices'][-1].message["content"]})
                st.markdown("\n######### enrepreneur #########\n")
                st.markdown("{}".format(ent_res['choices'][-1].message["content"]))
                investor_msgs.append({"role": "user", "content": ent_res['choices'][-1].message["content"]})
                investor_res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages= investor_msgs)
                investor_msgs.append({"role": "assistant", "content": ent_res['choices'][-1].message["content"]})
                st.markdown("\n#########  investor: #########\n")
                st.markdown("{}".format(investor_res['choices'][-1].message["content"]))
                ent_msgs.append({"role": "user", "content": investor_res['choices'][-1].message["content"]})
     
            

        except OpenAIError as e:
            st.error(e._message)
        
            