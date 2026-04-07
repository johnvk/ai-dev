from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# --- BUILD VECTOR STORE ---
def build_vectorstore():
    print("📚 Loading ZZZ Insurance policy document...")

    loader = TextLoader("documents/policy.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"   Split into {len(chunks)} chunks ✅")

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings)
    print(f"   Indexed into ChromaDB ✅")

    return vectorstore

# --- RAG TOOL ---
# This wraps RAG as a callable function the agent can use
def build_rag_tool(vectorstore):
    from langchain_core.tools import tool

    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a ZZZ Insurance policy expert.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say 'I cannot find that information in the policy document.'

Context:
{context}"""),
        ("user", "{question}")
    ])

    @tool
    def search_policy(question: str) -> str:
        """Search the ZZZ Insurance policy document to answer questions
        about coverage, exclusions, claims process, premiums, or renewals.
        Use this when the user asks anything about what the policy covers."""
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_chunks = retriever.invoke(question)
        context = "\n".join([chunk.page_content for chunk in relevant_chunks])

        chain = prompt | llm
        response = chain.invoke({
            "context": context,
            "question": question
        })
        return str(response.content)

    return search_policy