import streamlit as st
from streamlit.logger import get_logger
import superpowered
import os
import datetime

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

    with st.sidebar:
        st.write("hi")
        st.button("start new chat")
        # st.write(st.session_state)
            

    st.write("# Hi, I am Gilbert, your LLM GTM expert 👋")

    st.markdown(
        """
I have read every single blog post from MadKudu and OpenView.
I know a lot about GTM strategy, product-led growth, ABM, sales playbooks, etc.
    """
    )

    st.write(datetime.datetime.now().strftime("%H:%M:%S"))

    thread_id = ''
    if "thread_id" not in st.session_state:
        thread_id = "c2fc2461-5377-4a90-8a4a-579ae40aae3f"

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    rewriting_the_chat_current_role = 'user'
    current_chat_message = ''
    for msg in st.session_state.messages:
        if rewriting_the_chat_current_role != msg["role"]:
            current_chat_message = st.chat_message(msg["role"])
        rewriting_the_chat_current_role = msg["role"]
        if msg.get("action") == "expander":
            with current_chat_message.expander(msg["title"]):
                st.markdown(msg["content"])            
        else:
            current_chat_message.write(msg["content"])


    if prompt := st.chat_input(placeholder="How do you make ABM and PLG work together?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response = ''
        with st.spinner('Checking my sources...'):
            response = chat(thread_id, prompt)

            st.session_state.messages.append({"role": "assistant", "content": response["model_response"]["content"]})
            assistant_message = st.chat_message("assistant")
            assistant_message.write(response["model_response"]["content"])
        
            
            if response["ranked_results"]:
                for index, result in enumerate(response["ranked_results"]):
                    source_title = "Segment #" + str(index+1) + " from " + result["metadata"]["document"]["title"]
                    with assistant_message.expander(source_title):
                        st.session_state.messages.append({"role": "assistant", "action": "expander", "title": source_title, "content": result["metadata"]["original_content"]})
                        st.markdown(result["metadata"]["original_content"])                        
            
            del response

if __name__ == "__main__":
    run()
