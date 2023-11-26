import datetime
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import superpowered
import os
from sqlalchemy import text
import time
import streamlit as st
import json

COOKIE_NAME = 'superpowered_thread_id'

# cookie_manager = stx.CookieManager()

# @st.cache_resource
def get_sql_connection(): 
    return st.connection("postgresql", type="sql", ttl=1)

def get_saved_messages_from_thread(thread_id):
    with st.spinner('Fetching session info'):
        st.cache_data.clear()
        conn = get_sql_connection()
        conn.reset()
        df = conn.query(f"SELECT * FROM chat_threads WHERE thread_id ='{thread_id}' ")
        st.write('message response')
        st.write(df)
        st.write(df.shape)
        messages = None
        try:
            messages = df.head(1)['chat_history'].iloc[0]
        except:
            True
            # messages = [{"role": "assistant", "content": "How can I help you?"}]  
        return messages


def session_initialize():
    # with st.empty():
    #     cookie_thread_id = cookie_manager.get(cookie=COOKIE_NAME)
    #     # Not ideal but wait for cookies to be found before moving forward
    #     # this seems to be a known issue with Streamlit
    #     # see here for example: https://discuss.streamlit.io/t/finally-i-find-a-right-way-to-use-extra-cookie-manager/47094/3
    #     start_time = time.time()  # Capture the start time
    #     cookies = cookie_manager.get_all()
    #     with st.spinner('looking for past session'):
    #         while len(cookies) == 0:
    #             if time.time() - start_time > 7:  # Check if 7 seconds have passed
    #                 break  # Break the loop if more than 7 seconds have passed
    #     st.write(f'cookie thread id: {cookie_thread_id}')


    with st.spinner('Initializing session'):
        # If there is a thread_id in the session state, do nothing
        if "thread_id" in st.session_state:
            return
        # If there is no thread_id in the session state but there is a cookie with it, 
        # then fetch the right info from Postgres and update the session state
        elif cookie_thread_id:
            st.write('Past thread found.')
            st.session_state["thread_id"] = cookie_thread_id
            messages = get_saved_messages_from_thread(cookie_thread_id)
            if messages:
                st.write(messages)
                st.session_state["messages"] = json.loads(messages)
            else: 
                st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]  
            

        # if there is no thread_id in the session state or in cookie, create one and update cookie
        else:
            thread = create_new_thread(st)


# def session_save(st):
#     messages = st.session_state["messages"]
#     thread_id = st.session_state["thread_id"]
#     conn = st.connection("postgresql", type="sql")

#     with conn.session as session:
#             messages_as_json = json.dumps(messages)

#             sql = text(f"""INSERT INTO chat_threads (thread_id, chat_history) 
#                 VALUES (:thread_id, :messages)
#                 ON CONFLICT (thread_id) 
#                 DO UPDATE SET chat_history = EXCLUDED.chat_history;
#             """)
#             session.execute(sql, {"thread_id": thread_id, "messages": messages_as_json})
#             session.commit()    
#             st.write('Thread saved')


def create_new_thread():

    if 'thread_id' not in st.session_state:

        response = superpowered.create_chat_thread(
            knowledge_base_ids = ['0bf666e5-c187-4ad7-9a81-fad21427c39e'],
            model = 'gpt-4'                
        )

        thread_id = response["id"]
        st.session_state["thread_id"] = thread_id
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    # with st.empty():
    #     expirate_at = datetime.now() + timedelta(days=365)
    #     cookie_manager.set(COOKIE_NAME, thread_id, expires_at=expirate_at)         

    # session_save(st)
    

    