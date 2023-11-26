import streamlit as st


def refresh_chat_widget():
    rewriting_the_chat_current_role = 'user'
    current_chat_message = ''
    
    if 'messages' not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]  
    
    for msg in st.session_state.messages:
        if rewriting_the_chat_current_role != msg["role"]:
            current_chat_message = st.chat_message(msg["role"])
        rewriting_the_chat_current_role = msg["role"]
        if msg.get("action") == "expander":
            with current_chat_message.expander(msg["title"]):
                st.markdown(msg["content"])            
        else:
            current_chat_message.write(msg["content"])

