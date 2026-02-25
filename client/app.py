import streamlit as st
from utils.api import upload_pdfs, ask_question

st.set_page_config(
  page_title="RagBot Chat Bot ",
  page_icon="🤖",
  layout="centered"
)

#main title
st.title(" RagBot 2.0 — Chat with your PDF")
st.markdown("Upload PDFs, ask questions, and get answers in seconds!")
st.divider()

#Sidebar pdf upload
st.sidebar.header("Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF file(s)",
    type="pdf",
    accept_multiple_files=True
)

if st.sidebar.button("Upload & Index PDF"):
    if uploaded_files:
        with st.spinner("Uploading and indexing... please wait"):
            result = upload_pdfs(uploaded_files)
        st.sidebar.success(result.get("message", "Done!"))
    else:
        st.sidebar.warning("Please select at least one PDF first!")

# ── MAIN — Chat Section ───────────────────────────────

# Initialize chat history in session state
# This keeps history even when page reruns
if "history" not in st.session_state:
    st.session_state.history = []    

# Question input
question = st.text_input(
    "Ask a question about your PDF:",
    placeholder="e.g. What is this document about?"
)

# Buttons side by side
col1, col2 = st.columns([1, 5])

ask_btn   = col1.button("Ask 🤔")
clear_btn = col2.button("Clear History 🗑️")


# When Ask button clicked

# When Ask button clicked
if ask_btn and question:
    with st.spinner("Thinking..."):
        answer = ask_question(question)
    # Save to history
    st.session_state.history.append({
        "q": question,
        "a": answer
    })

# When Clear button clicked
if clear_btn:
    st.session_state.history = []
    st.success("History cleared!")    

# Show chat history — newest first
if st.session_state.history:
    st.subheader("💬 Chat History")
    for chat in reversed(st.session_state.history):
        st.markdown(f"**🙋 You:** {chat['q']}")
        st.markdown(f"**🤖 Bot:** {chat['a']}")
        st.divider()
else:
    st.info("Upload a PDF and ask your first question!")    