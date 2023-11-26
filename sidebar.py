from session_management import create_new_thread

def add_sidebar(st):

    with st.sidebar:

        st.write("# Hi, I am Gilbert, your LLM GTM expert 👋")

        st.markdown(
            """
    I have read every single blog post from MadKudu and OpenView.
    I know a lot about GTM strategy, product-led growth, ABM, sales playbooks, etc.
        """
        )

        btn_new_chat = st.button("\+ new chat thread")
        if btn_new_chat:
            response = create_new_thread(force_refresh=True)

