import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import http.cookies
import time
import uuid

# https://discuss.streamlit.io/t/new-component-streamlit-js-eval/30861

def get_cookie_value(cookie_string, cookie_name):
    # Create a SimpleCookie object
    cookie = http.cookies.SimpleCookie()
    cookie.load(cookie_string)

    # Extract and return the value of the specified cookie
    if cookie_name in cookie:
        return cookie[cookie_name].value
    else:
        return None

def get_session_cookie():
    start_time = time.time()
    cookies = ""
    
    cookies = streamlit_js_eval(js_expressions="document.cookie", want_output = True)
    # cookies = st_javascript("document.cookie", key=str(uuid.uuid4()))
    while time.time() - start_time < 7:
        if cookies:  # Check if cookies are populated            
            break
        time.sleep(0.5)  # Wait for 0.5 seconds before checking again

    cookie_name = "superpowered_thread_id"
    thread_id = get_cookie_value(cookies, cookie_name)
    
    return thread_id


def set_session_cookie(thread_id):

    cookie_name = "superpowered_thread_id"

    javascript_to_set_session_cookie = f'''
    let expires = "";

    let days = 30;

    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
    
    document.cookie = "{cookie_name}" + "=" + "{thread_id}"  + expires + "; path=/";
    '''


    res = streamlit_js_eval(js_expressions=javascript_to_set_session_cookie)

