import streamlit as st
from streamlit.logger import get_logger
import superpowered
import os
# import datetime


from sidebar import add_sidebar 
from session_management import session_initialize, session_save
from refresh_chat import refresh_chat_widget

# Check if environment variables are set, otherwise use Streamlit secrets
if not os.getenv("SUPERPOWERED_API_KEY_ID") or not os.getenv("SUPERPOWERED_API_KEY_SECRET"):
    os.environ["SUPERPOWERED_API_KEY_ID"] = st.secrets.SUPERPOWERED_API_KEY
    os.environ["SUPERPOWERED_API_KEY_SECRET"] = st.secrets.SUPERPOWERED_SECRET_KEY

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
        page_title="Carol, your AI-powered CMO assistant",
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
        with st.spinner('Hold tight. Analyzing thousands of posts...'):
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
                        st.session_state.messages.append({"role": "assistant", "action": "expander", "title": source_title, "content": result["metadata"]["original_content"], "source_url": source_url})
                        st.markdown(result["metadata"]["original_content"], unsafe_allow_html=True)                        
            
            del response
            session_save()

if __name__ == "__main__":
    run()
