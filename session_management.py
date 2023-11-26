import datetime
import superpowered
from sqlalchemy import text
import streamlit as st
import json
import os

from cookie_utils import get_session_cookie, set_session_cookie

COOKIE_NAME = 'superpowered_thread_id'

def get_sql_connection(): 
    os.environ["pg_host"] = st.secrets.pg_host
    os.environ["pg_port"] = st.secrets.pg_port
    os.environ["pg_db"] = st.secrets.pg_db
    os.environ["pg_username"] = st.secrets.pg_username
    os.environ["pg_password"] = st.secrets.pg_password

    conn = st.connection(
        'postgres',
        type = "sql",
        dialect = "postgresql",
        host = os.environ["pg_host"],
        port = os.environ["pg_port"],
        database = os.environ["pg_db"],
        username = os.environ["pg_username"],
        password = os.environ["pg_password"]
    )

    return conn

def get_saved_messages_from_thread(thread_id):
    st.cache_data.clear()
    conn = get_sql_connection()
    conn.reset()
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
                st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]  
            
        # if there is no thread_id in the session state or in cookie, create one and update cookie
        else:
            thread = create_new_thread()


def session_save():
    messages = st.session_state["messages"]
    thread_id = st.session_state["thread_id"]
    conn = st.connection("postgresql", type="sql")

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
            model = 'gpt-4'                
        )

        thread_id = response["id"]
        st.session_state["thread_id"] = thread_id
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    st.sidebar.write('New thread id ' + st.session_state["thread_id"])

    set_session_cookie(st.session_state["thread_id"])

    

    