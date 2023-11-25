import streamlit as st
from streamlit.logger import get_logger
import superpowered

LOGGER = get_logger(__name__)

print(st.secrets)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Revenue Brainiac LLM! 👋")

    st.markdown(
        """
Hi, I'm a chatbot who have read every single blog post from MadKudu and OpenView.
I know a lot about GTM strategy, product-led growth, ABM, sales playbooks, etc.
    """
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


# # Initialize API key and secret
# os.environ["SUPERPOWERED_API_KEY_ID"]="INSERT_API_KEY_ID_HERE"
# os.environ["SUPERPOWERED_API_KEY_SECRET"]="INSERT_API_KEY_SECRET_HERE"

# # Make the request for the desired chat thread and message
# response = superpowered.get_chat_response(
#     thread_id="c2fc2461-5377-4a90-8a4a-579ae40aae3f",
#     input="",
# )

# # Print the response
# print (response["interaction"]["model_response"]["content"])

    if prompt := st.chat_input(placeholder="How do you make ABM and PLG work together?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("<a>yoyo</a>")

        # if not openai_api_key:
        #     st.info("Please add your OpenAI API key to continue.")
        #     st.stop()

        # llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
        # search = DuckDuckGoSearchRun(name="Search")
        # search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
        # with st.chat_message("assistant"):
        #     st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        #     response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        #     st.session_state.messages.append({"role": "assistant", "content": response})
        #     st.write(response)


if __name__ == "__main__":
    run()
