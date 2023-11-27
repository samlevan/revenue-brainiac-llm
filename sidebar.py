import streamlit as st
from session_management import create_new_thread
from sql_utils import get_sql_connection
from sqlalchemy import text
import time



def add_sidebar(st):

    with st.sidebar:

        btn_new_chat = st.button("\\+ New thread")
        if btn_new_chat:
            response = create_new_thread(force_refresh=True)


        st.write("# Hi, I am Carol 👋")

        st.markdown(
            """
            I am an AI. 
            
            My goal is to help marketing leaders think about GTM strategy, product-led growth, ABM, sales playbooks, etc.
            
            I might be the first AI to do so.
        """)

        st.divider()

        st.markdown("""What makes me special?""")    

        with st.expander('1️⃣ I specialize in Sales & Marketing.'):
            st.markdown("""I have read hundreds of curated blog posts on the subject. Those posts were written by GTM leaders 
            like [MadKudu](https://madkudu.com) and [OpenView](https://www.openviewpartners.com). And I keep learning more and more about Sales and Marketing.
        """, unsafe_allow_html=True)

        with st.expander('2️⃣ I share my sources.'):
            st.markdown("""I am an AI and I am sometimes wrong. This is why I share what I used to craft answers. 
                    It makes it easy for you to check what I share. Additionaly, those sources are often very interesting posts to read too if you want to get deeper on a topic.
        """, unsafe_allow_html=True)

        with st.expander('3️⃣ I can learn from you.'):
            st.markdown("""Paste the URL of content you'd like me to study. I will add this to my knowledge base to become smarter when you come back.
        """, unsafe_allow_html=True)

            def send_url_to_study(url):
                thread_id = st.session_state["thread_id"]
                conn = get_sql_connection()
                with conn.session as session:
                    sql = text(f"""INSERT INTO urls_to_learn (thread_id, url) VALUES (:thread_id, :url)""")
                    session.execute(sql, {"thread_id": thread_id, "url": url})
                    session.commit()    

            with st.form("send-url-form", clear_on_submit=True):
                url = st.text_input('URL:', placeholder = 'e.g. https://www.madkudu.com/blog/5-steps-warm-outbound-play')
                submit_button = st.form_submit_button("Submit")

                if submit_button:
                    send_url_to_study(url)
                    success_message = st.empty()
                    success_message.success(url + ' sent!')
                    time.sleep(2)
                    success_message.empty()


        st.divider()

        st.markdown('Have feedback? ')

        with st.expander('Help me be a better partner 🙏'):

            def send_feedback_to_carol(feedback):
                thread_id = st.session_state["thread_id"]
                conn = get_sql_connection()
                with conn.session as session:
                    sql = text(f"""INSERT INTO feedback_on_carol (thread_id, feedback) VALUES (:thread_id, :feedback)""")
                    session.execute(sql, {"thread_id": thread_id, "feedback": feedback})
                    session.commit()    

            st.markdown('Share what you like and how I can improve')

            with st.form("send-feedback-form", clear_on_submit=True):
                feedback = st.text_area('Feedback:')
                submit_feedback_button = st.form_submit_button("Submit")

                if submit_feedback_button:
                    send_feedback_to_carol(feedback)
                    success_message = st.empty()
                    success_message.success('Feedback received. Thanks!')
                    time.sleep(2)
                    success_message.empty()



        st.divider()

        st.markdown("Made with ❤️ by the people at [MadKudu](https://madkudu.com)")


        with st.expander('Credit'):
            credit = """
            - [OpenView](https://www.openviewpartners.com) for the fantastic content they have published over the years. This AI read lots of it.
            - [Streamlit](https://streamlit.io/) for making it very easy to build apps like this.
            """
            st.markdown(credit, unsafe_allow_html=True)

        disclaimer = '<p style="font-size: 10px;">This LLM can make mistakes. Consider checking important information.</p>'
        st.markdown(disclaimer, unsafe_allow_html=True)