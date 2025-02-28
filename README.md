# Custom Data-Driven Chatbot

Welcome to the **Custom Data-Driven Chatbot** repository! This project allows you to create a chatbot that leverages your own data (PDFs, TXT files, CSVs, etc.) to provide context-aware responses. The chatbot is built using **LangChain** and **Gradio**, and it supports memory, document retrieval, and database management.

## Features
- **Custom Data Integration**: Load and process your own documents (PDFs, TXTs, CSVs, DOCX, XLSX).
- **Memory**: An option to update the database with the conversation history. 
- **Database Management**: Create and update the chatbot's database.
- **User-Friendly Interface**: Built with Gradio for an intuitive and interactive UI.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8 or higher**
- **OpenAI API Key**: You need an API key from OpenAI to use the GPT-4 model.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/custom-data-driven-chatbot.git
   cd custom-data-driven-chatbot
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install gradio langchain openai pypdf unstructured python-docx pandas numpy tqdm sentence-transformers
   ```

4. **Set Up Your OpenAI API Key**:
   - Add your OpenAPI key in the  `openai_api_key` variable in the script "chatbot.py" with your actual OpenAI API key.

## Usage

### 1. Prepare Your Data
- Place your data files (PDFs, TXTs, CSVs, DOCX, XLSX) in the `Data` folder.

### 2. Run the Chatbot
- Start the chatbot by running the script:
  ```bash
  python chatbot.py
  ```
- The chatbot will launch a Gradio interface in your browser at `http://127.0.0.1:7860/`.

### 3. Create the Database
- For the first time you use the chatbot, press on the button "Create/Update Database (Using your own files)" to create the database. 
- For any new files/docs you want to incroporate in the database, add these to the 'Data' folder and press again on the 'Create/Update Database (Using your own files)' button, you can delete the files/docs from 'Data' folder after updating the database. 

### 4. Interact with the Chatbot
- Type your questions in the chat interface.
- The chatbot will retrieve relevant information from your data and provide responses.

### 4. Manage the Database
- **Create/Update Database**: Click the "Create/Update Database" button to process your data and update the chatbot's knowledge base.
- **Update Memory**: Click the "Update Memory" button to save the conversation history to the database.

### 5. Clear Conversation History
- Use the "Clear History" button to delete the conversation history. Note that If you have previously updated memory, the database will have to be deleted to clear the data and re-created from scratch. 

## Folder Structure
- **`Data`**: Place your data files (PDFs, TXTs, CSVs, DOCX, XLSX) here.
- **`Database`**: Stores the database files. Do not modify this folder manually.
- **`Memory`**: Stores the conversation history and memory files.
- **`chatbot.py`**: The main script for the chatbot.

## Customization

### Change the Chatbot's Name and Description
- Modify the `title` and `description` parameters in the `gr.ChatInterface` section of the script:
  ```python
  chatbot_ui = gr.ChatInterface(
      fn=chatbot_response,
      title="Your Custom Title",
      description="Your custom description.",
      theme="soft"
  )
  ```

### Add More File Types
- To support additional file types, add new `DirectoryLoader` instances in the `create_update_database` function.

### Change the Model
- Replace `"gpt-4o"` in the `ChatOpenAI` initialization with another model (e.g., `"gpt-4", "gpt-4o-mini"`).

## Troubleshooting

### 1. **Database Not Updating**
- Ensure your data files are in the `Data` folder and have valid content.
- Check the console for any error messages.

### 2. **Chatbot Not Responding**
- Verify that your OpenAI API key is correct and has sufficient credits.
- Ensure the database is created/updated before interacting with the chatbot.

### 3. **Browser Not Opening**
- If the browser does not open automatically, manually navigate to `http://127.0.0.1:7860/`.


## Running the Chatbot with a `.bat` File (Windows)

To make it easier to run the chatbot on your computer, you can create a `.bat` file. Here’s how:

1. **Create a `.bat` File**:
   - Open Notepad or any text editor.
   - Paste the following script:
     ```batch
     @echo off
     "C:\Users\XYZ\miniconda3\python.exe" "D:/Directory/chatbot.py"
     timeout /t 5 /nobreak >nul
     start http://127.0.0.1:7860/
     ```
   1.1 **Replace the Python Directory**  
      Replace the placeholder `C:\Users\XYZ\miniconda3\python.exe` with your actual Python installation path.  
      You can find your Python directory using one of the following methods:
   
      - **Via Python Script in IDE:**
        Run the following script in your Python IDE or interpreter:
        ```python
        import sys
        print("Python Directory:", sys.executable)
        ```
   
      - **Using the `which` Command (Linux/Mac) or `where` Command (Windows):**
        - **Linux/Mac:**
          ```bash
          which python
          ```
        - **Windows:**
          ```batch
          where python
          ```
   1.2 **Replace the Repository Directory**  
      Replace the placeholder `D:/Directory/chatbot.py` with the directory where this repository is located on your machine.  
      For example, if you cloned the repository to `C:/Projects/chatbot`, update the path accordingly.
       
2. **Save the File**:
   - Save the file with a `.bat` extension, e.g., `run_chatbot.bat`.
   - Make sure to select "All Files" in the "Save as type" dropdown to avoid saving it as a `.txt` file.

3. **Run the `.bat` File**:
   - Double-click the `run_chatbot.bat` file to run the chatbot.
   - The script will:
     - Run the `chatbot.py` script.
     - Wait for 5 seconds to ensure the server is ready.
     - Open your default browser to `http://127.0.0.1:7860/`.


## Contributing

Contributions are welcome! 

---
Enjoy using your **Custom Data-Driven Chatbot**! If you have any questions or issues, feel free to open an issue on GitHub.
---
Let me know if you need further assistance! 😊
