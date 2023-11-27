import streamlit as st
import os

def get_sql_connection(): 
    if not os.getenv("pg_host"):
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
    conn.reset()

    return conn