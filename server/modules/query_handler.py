from modules.load_vectorstore import load_vectorstore
from modules.llm import get_llm
from langchain_core.messages import HumanMessage

def answer_query(question: str):
    db = load_vectorstore()
    docs = db.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = (
        "Use the following context to answer the question.\n"
        "If the answer is not in the context, say 'I don't know based on the provided document.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content