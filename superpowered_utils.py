import superpowered

def create_new_thread(st):
    response = superpowered.create_chat_thread(
        knowledge_base_ids = ['0bf666e5-c187-4ad7-9a81-fad21427c39e'],
        model = 'gpt-4'                
    )
    st.session_state["thread_id"] = response["id"]
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]
    return response
