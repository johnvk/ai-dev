from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings()

# --- PHASE 1: INDEXING ---
print("📚 Loading and indexing document...")

# Step 1 — Load the document
loader = TextLoader("policy.txt")
docs = loader.load()
print(f"  Loaded: {len(docs)} document")

# Step 2 — Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)
print(f"  Split into: {len(chunks)} chunks")

# Step 3 — Store in ChromaDB (generates embeddings automatically)
vectorstore = Chroma.from_documents(chunks, embeddings)
print(f"  Indexed into ChromaDB ✅")

# --- PHASE 2: RETRIEVAL ---
print("\n🔍 Starting Q&A...\n")

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an ZZZ Insurance assistant.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say 'I cannot find that information in the policy.'

Context:
{context}"""),
    ("user", "{question}")
])

def ask(question):
    # Find the most relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    relevant_chunks = retriever.invoke(question)

    # Combine chunks into context
    context = "\n".join([chunk.page_content for chunk in relevant_chunks])

    # Generate answer
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })

    print(f"Q: {question}")
    print(f"A: {response.content}")
    print()

# Test it with real questions
ask("Does the policy cover flood damage?")
ask("How long does it take to process a claim?")
ask("What is the maximum no-claim discount?")
ask("Is mechanical breakdown covered?")
ask("Does the policy cover earthquake damage?")