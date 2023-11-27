import datetime
import superpowered
import streamlit as st
import json
from sqlalchemy import text

from cookie_utils import get_session_cookie, set_session_cookie
from sql_utils import get_sql_connection

COOKIE_NAME = 'superpowered_thread_id'
FIRST_MESSAGE = """What sales or marketing question is on your mind?

For example:
For example:
- What key signals should I look at to identify accounts to go after?
- When is it better to use PQLs vs PQAs?
- What's the alternative to cold outbound?
laptop, laptop and browser it up sad"""


def get_saved_messages_from_thread(thread_id):
    st.cache_data.clear()
    conn = get_sql_connection()
    df = conn.query(f"SELECT * FROM chat_threads WHERE thread_id ='{thread_id}' ", show_spinner=False)
    messages = None
    try:
        messages = df.head(1)['chat_history'].iloc[0]
    except:
        True
    return messages


def session_initialize():

    cookie_thread_id = get_session_cookie()

    with st.spinner('Initializing session'):
        # If there is a thread_id in the session state, do nothing
        if "thread_id" in st.session_state:
            return
        # If there is no thread_id in the session state but there is a cookie with it, 
        # then fetch the right info from Postgres and update the session state
        elif cookie_thread_id:
            st.session_state["thread_id"] = cookie_thread_id
            messages = get_saved_messages_from_thread(cookie_thread_id)
            if messages:
                st.session_state["messages"] = json.loads(messages)
            else: 
                st.session_state["messages"] = [{"role": "assistant", "content": FIRST_MESSAGE}]  
            
        # if there is no thread_id in the session state or in cookie, create one and update cookie
        else:
            thread = create_new_thread()


def session_save():
    messages = st.session_state["messages"]
    thread_id = st.session_state["thread_id"]
    conn = get_sql_connection()

    with conn.session as session:
            messages_as_json = json.dumps(messages)

            sql = text(f"""INSERT INTO chat_threads (thread_id, chat_history) 
                VALUES (:thread_id, :messages)
                ON CONFLICT (thread_id) 
                DO UPDATE SET chat_history = EXCLUDED.chat_history;
            """)
            session.execute(sql, {"thread_id": thread_id, "messages": messages_as_json})
            session.commit()    


def create_new_thread(force_refresh=False):

    if 'thread_id' not in st.session_state or force_refresh:

        response = superpowered.create_chat_thread(
            knowledge_base_ids = ['0bf666e5-c187-4ad7-9a81-fad21427c39e'],
            model = 'gpt-4',
            system_message="""You are a marketing advisor. 

            Use the sources you have access to as much as possible. Prioritize the context you are given to answer questions.

            Do not write things like "[Source 102]" to refer to the sources used."""
        )

        thread_id = response["id"]
        st.session_state["thread_id"] = thread_id
        st.session_state["messages"] = [
            {"role": "assistant", "content": FIRST_MESSAGE}
        ]

    st.sidebar.write('New thread id ' + st.session_state["thread_id"])

    set_session_cookie(st.session_state["thread_id"])

    

    