# HR Policy & Leave Conversational Assistant

## Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- Ollama installed and running locally

### Installation Steps

1. **Install Ollama** (if not already installed)
   ```bash
   # Visit https://ollama.ai to download and install
   # Or use the appropriate installer for your OS
   ```

2. **Pull an LLM model**
   ```bash
   ollama pull mistral
   # Or try: llama2, llama3, phi
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

### Usage

1. Click "Initialize Agent" in the sidebar
2. Wait for the agent to load (first time may take 30-60 seconds)
3. Start asking questions about HR policies!
4. Try example questions from the sidebar

### Example Questions
- "What is the annual leave policy?"
- "How many sick leave days do I get?"
- "How do I apply for work from home?"
- "What are the working hours?"
- "What about casual leave?" (follow-up question)

### Troubleshooting

**Agent fails to initialize:**
- Ensure Ollama is running: `ollama serve`
- Check if the model is pulled: `ollama list`
- Verify network connection to localhost:11434

**Slow responses:**
- First query is always slower (model loading)
- Consider using a smaller model like `phi` for faster responses
- Ensure no other heavy applications are running

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're in the correct directory

### Project Structure
```
agentic/
├── app.py                    # Streamlit UI application
├── agent/
│   ├── __init__.py
│   ├── hr_agent.py          # Main agent implementation
│   ├── tools.py             # Policy retrieval tools
│   └── prompts.py           # Agent prompts
├── data/
│   └── policies/            # HR policy documents
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

### Features
✅ Conversational AI with context memory  
✅ ReAct agent pattern (Reasoning + Acting)  
✅ Local LLM via Ollama (zero cost, private)  
✅ Semantic search over policy documents  
✅ Professional Streamlit UI  
✅ Follow-up question handling  

### Customization

**Add new policy documents:**
- Add `.txt` files to `data/policies/` directory
- Restart the agent to reload documents

**Change LLM model:**
- Select different model from sidebar dropdown
- Reinitialize the agent

**Adjust agent behavior:**
- Edit prompts in `agent/prompts.py`
- Modify agent parameters in `agent/hr_agent.py`

---

**Note:** This is a demonstration project. For production use, consider adding authentication, logging, and integration with actual HR systems.
