import streamlit as st

FIRST_MESSAGE = """What sales or marketing question is on your mind?

For example:
- What key signals should I look at to identify accounts to go after?
- When is it better to use PQLs vs PQAs?
- How do you make ABM and PLG work together?
"""

def refresh_chat_widget():
    rewriting_the_chat_current_role = 'user'
    current_chat_message = ''
    
    if 'messages' not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": FIRST_MESSAGE}]  
    
    for msg in st.session_state.messages:
        if rewriting_the_chat_current_role != msg["role"]:
            current_chat_message = st.chat_message(msg["role"])
        rewriting_the_chat_current_role = msg["role"]
        if msg.get("action") == "expander":
            with current_chat_message.expander(msg["title"]):
                if "source_url" in msg:
                    source_url = msg["source_url"]
                    st.write(f'source: <a href="{source_url}">{source_url}</a>', unsafe_allow_html=True)
                st.markdown(msg["content"])            
        else:
            current_chat_message.write(msg["content"])

