import gradio as gr
import os
from langchain.document_loaders import DirectoryLoader, CSVLoader, UnstructuredExcelLoader
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
import webbrowser
import threading
import time

# Get the current working directory
current_directory = os.getcwd()
# === File Paths ===
openai_api_key = "ADD YOUR OPENAI API KEY HERE"
DB_PATH = current_directory+"/Database"
DATA_PATH = current_directory+"/Data"
Memory_Path = current_directory+"/Memory"
Historylog= Memory_Path+"/Historylog.txt"


# Function to open the browser after a delay
def open_browser():
    time.sleep(5)  # Wait for 5 seconds to ensure the server is ready
    webbrowser.open("http://127.0.0.1:7860/")

# Start the browser in a separate thread
threading.Thread(target=open_browser).start()

# === Function to Save History ===
def save_history(message):
    # Open the file in append mode and add the message
    with open(Historylog, "a") as f:
        f.write(f"{message}\n")
        
# === Load Stored Embeddings ===
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectordb = Chroma(persist_directory=DB_PATH, embedding_function=embedding)

# === Create a Retriever ===
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# === Load the Language Model ===
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, openai_api_key=openai_api_key)

# === Add Memory for Conversational Context ===
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"  # Ensures only "answer" is stored in memory
)

# === Set up the Conversational Chain ===
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True  # Enables both database and general AI reasoning
)

# === Load Conversation History ===
conversation_history = []

# === Gradio Chatbot Function ===
def chatbot_response(message, history):
    """Handles user messages and returns chatbot responses."""
    
    response = qa_chain.invoke({"question": message, "chat_history": conversation_history})

    # Update conversation history
    conversation_history.append((message, response["answer"]))

    if isinstance(response, tuple):
        response = response[0]  # Extract the first element if it's a tuple
    elif isinstance(response, dict) and "answer" in response:
        response = response["answer"]
        
    save_history(f"User: {message}\n")
    save_history(f"Chatbot: {response}\n")

    return str(response)   # Return updated history list

# === Gradio UI ===
# chatbot_ui.launch(share=True)#to share with others
def Update_Memory():
    docs=[]
    txt_loader = DirectoryLoader(Memory_Path, glob="*.txt", loader_cls=TextLoader)
    docs.extend(txt_loader.load())
    # Check if new documents exist
    if docs:
        print("📂 Updating Memory - Processing...")
        # Split new text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        # ✅ Add new documents to the existing database
        vectordb.add_documents(chunks)
        # ✅ Persist the updated database
        vectordb.persist()
        print("✅ Memory updated successfully!")
    else:
        print("🚀 Memory is already up to date.")
        
def Clear_History():        
    with open(Historylog, "w") as f:
        pass  # Opening in "w" mode and doing nothing clears the file

def create_update_database():
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Check if database exists
    if os.path.exists(DB_PATH):
        print("📂 Database found. Updating with new documents...")
        vectordb = Chroma(persist_directory=DB_PATH, embedding_function=embedding)
    else:
        print("🚀 No database found. Creating a new one...")
        os.makedirs(DB_PATH, exist_ok=True)
        vectordb = None  # Initialize as None for now

    # Load documents
    docs = []

    # Load PDF files
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    docs.extend(pdf_loader.load())

    # Load TXT files
    txt_loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    docs.extend(txt_loader.load())

    # Load CSV files
    csv_loader = DirectoryLoader(DATA_PATH, glob="*.csv", loader_cls=CSVLoader)
    docs.extend(csv_loader.load())

    # Load DOCX files
    docx_loader = DirectoryLoader(DATA_PATH, glob="*.docx", loader_cls=UnstructuredWordDocumentLoader)
    docs.extend(docx_loader.load())

    # Load XLSX files
    xlsx_loader = DirectoryLoader(DATA_PATH, glob="*.xlsx", loader_cls=UnstructuredExcelLoader)
    docs.extend(xlsx_loader.load())

    # Check if new documents exist
    if not docs:
        print("✅ No new documents found. Database is up to date.")
    else:
        print(f"📄 Found {len(docs)} new documents. Processing...")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        # Add to the existing database or create a new one
        if vectordb:
            vectordb.add_documents(chunks)
        else:
            vectordb = Chroma.from_documents(chunks, embedding, persist_directory=DB_PATH)
        # Save changes
        vectordb.persist()
        print("✅ Database updated successfully!") 
        
with gr.Blocks() as ChatWeb:
    # Add the ChatInterface
    chatbot_ui = gr.ChatInterface(
        fn=chatbot_response,
        title="Your Custom Title",
        description="Your custom description.",
        theme="soft"
    )

    # Add a "Update Memory" button
    Update_MemoryButton = gr.Button("Update Memory (Save Context of Conversations in Database)")
    Update_MemoryButton.click(
        Update_Memory,  # Function to call   
    )
    
    # Add a "Clear_History" button
    Clear_HistoryButton = gr.Button("Clear History (Clear Conversations History)")
    Clear_HistoryButton.click(
        Clear_History,  # Function to call   
    )
    
    # Create/Update a database based on your data - add buttpm
    CU_DB_Button = gr.Button("Create/Update Database (Using your own files)")
    CU_DB_Button.click(
        create_update_database,  # Function to call   
    )
    

ChatWeb.launch(server_name="0.0.0.0", server_port=7860, share=False)
