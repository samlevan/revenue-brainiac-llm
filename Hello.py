import streamlit as st
from streamlit.logger import get_logger
import superpowered
import os

# Initialize API key and secret
os.environ["SUPERPOWERED_API_KEY_ID"] = st.secrets.SUPERPOWERED_API_KEY
os.environ["SUPERPOWERED_API_KEY_SECRET"]= st.secrets.SUPERPOWERED_SECRET_KEY

LOGGER = get_logger(__name__)

def chat(prompt):
    # Make the request for the desired chat thread and message
    response = superpowered.get_chat_response(
        thread_id="c2fc2461-5377-4a90-8a4a-579ae40aae3f",
        input=prompt
    )

    # Print the response
    return response["interaction"]["model_response"]["content"]


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Hi, I am Graham, your LLM GTM expert 👋")

    st.markdown(
        """
I have read every single blog post from MadKudu and OpenView.
I know a lot about GTM strategy, product-led growth, ABM, sales playbooks, etc.
    """
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    if prompt := st.chat_input(placeholder="How do you make ABM and PLG work together?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("give me a few seconds... I am checking my sources...")
        response = chat(prompt)
        st.chat_message("assistant").write(response + "<br><a>sources</a>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        

if __name__ == "__main__":
    run()
