# 📊 Financial Document Q&A Assistant

This is a Streamlit web app that lets you **upload financial documents (PDF or Excel)** and then ask **questions in natural language** about revenue, expenses, profits, and other metrics.  
It extracts data from documents and uses **Ollama** (local LLMs like `mistral`) to answer your questions.

---

## 🚀 How to Run

### 1. Install Python & Ollama
- Install **Python 3.9+**  
- Install [Ollama](https://ollama.ai/)  
- Pull the mistral model:
  ```bash
  ollama pull mistral

2. Clone this repo
git clone https://github.com/your-username/financial-qa-assistant.git
cd financial-qa-assistant

3. Create environment & install dependencies
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

4. Start Ollama

Test the model works:

ollama run mistral

5. Run the app
streamlit run app.py


Then open your browser at http://localhost:8501

📂 Files

app.py → Streamlit interface

parsers.py → Extracts text & tables from PDF/Excel

qa_engine.py → Q&A engine with Ollama integration

utils.py → Helper functions

requirements.txt → Dependencies
