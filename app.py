import streamlit as st
from src.helper import get_pdf_text,get_text_chunks,get_vector_store,get_conversational_chain

def user_input(user_question):
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i%2 == 0:
            st.write("User: ",message.content)
        else:
            st.write("Reply: ",message.content)

def main():
    st.set_page_config("Information Retrieval")
    st.header("PDF information retriever", divider="gray")

    user_question = st.text_input("What do you want to know from the pdf file uploaded?")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("UPLOAD PDF:")
        pdf_docs = st.file_uploader("Upload your PDF files and click on the submit & process button",accept_multiple_files=True)
        if st.button("submit & process"):
            with st.spinner("processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)

                st.success("done")
if __name__ == "__main__":
    main()