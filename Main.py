import streamlit as st
from streamlit.logger import get_logger
import superpowered
import os
# import datetime


from sidebar import add_sidebar 
from session_management import session_initialize, session_save
from refresh_chat import refresh_chat_widget

# Initialize API key and secret
os.environ["SUPERPOWERED_API_KEY_ID"] = st.secrets.SUPERPOWERED_API_KEY
os.environ["SUPERPOWERED_API_KEY_SECRET"]= st.secrets.SUPERPOWERED_SECRET_KEY

LOGGER = get_logger(__name__)

def chat(thread_id, prompt):
    # Make the request for the desired chat thread and message
    response = superpowered.get_chat_response(
        thread_id=thread_id,
        input=prompt
    )

    # Print the response
    return response["interaction"]


def run():
    st.set_page_config(
        page_title="Gilbert, your AI GTM expert",
        page_icon="👋",
    )

    add_sidebar(st)

    session_initialize()

    refresh_chat_widget()

    
    if prompt := st.chat_input(placeholder="How do you make ABM and PLG work together?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        session_save()
        
        response = ''
        with st.spinner('Checking my sources...'):
            response = chat(st.session_state["thread_id"], prompt)

            st.session_state.messages.append({"role": "assistant", "content": response["model_response"]["content"]})
            assistant_message = st.chat_message("assistant")
            assistant_message.write(response["model_response"]["content"])
        
            if response["ranked_results"]:
                for index, result in enumerate(response["ranked_results"]):
                    source_title = "Segment #" + str(index+1) + " from " + result["metadata"]["document"]["title"]
                    with assistant_message.expander(source_title):
                        source_url = result["metadata"]["document"]["link_to_source"]
                        st.write(f'source: <a href="{source_url}">{source_url}</a>', unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "assistant", "action": "expander", "title": source_title, "content": result["metadata"]["original_content"]})
                        st.markdown(result["metadata"]["original_content"])                        
            
            del response
            session_save()

if __name__ == "__main__":
    run()
