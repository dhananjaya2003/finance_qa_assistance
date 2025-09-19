import streamlit as st
from parsers import extract_from_pdf, extract_from_excel
from qa_engine import QAEngine

st.set_page_config(page_title="Financial Document Q&A", layout='wide')
st.title("Financial Document Q&A Assistant")

if 'engine' not in st.session_state:
    st.session_state.engine = QAEngine()

with st.sidebar:
    uploaded_file = st.file_uploader("Upload PDF or Excel", type=["pdf","xlsx","xls"])
    st.session_state.ollama_model = st.text_input("Ollama model", value=st.session_state.get('ollama_model','mistral'))
    if st.button("Reinitialize QA Engine"):
        st.session_state.engine.reinit_model(st.session_state.ollama_model)

if uploaded_file:
    if uploaded_file.name.lower().endswith('.pdf'):
        st.session_state.raw_text, st.session_state.tables = extract_from_pdf(uploaded_file)
    else:
        st.session_state.raw_text, st.session_state.tables = extract_from_excel(uploaded_file)
    st.session_state.engine.index_document(st.session_state.raw_text, st.session_state.tables, uploaded_file.name)
    st.success("Document parsed successfully")

if st.session_state.get('raw_text'):
    st.subheader("Preview")
    st.text_area("Extracted Content", st.session_state.raw_text[:1500], height=250)

st.header("Chat")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg['role']).write(msg['content'])

query = st.chat_input("Ask a financial question")
if query:
    st.session_state.chat_history.append({'role':'user','content':query})
    answer = st.session_state.engine.answer_query(query)
    st.session_state.chat_history.append({'role':'assistant','content':answer})
    st.experimental_rerun()