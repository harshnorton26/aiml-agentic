# 🚀 Quick Start - HR Policy Assistant

## Step-by-Step Setup

### 1️⃣ Prerequisites Check

**Verify Python:**
```bash
python --version
# Should be 3.10 or higher
```

**Install Ollama:**
- Windows: Download from https://ollama.ai
- After installation, verify: `ollama --version`

### 2️⃣ Setup Ollama

```bash
# Pull the Mistral model (recommended)
ollama pull mistral

# Start Ollama service (if not running)
ollama serve
```

### 3️⃣ Install Dependencies

**Option A: Using Virtual Environment (Recommended)**
```bash
cd h:\aiml\agentic

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Option B: Direct Installation**
```bash
pip install langchain langchain-community ollama faiss-cpu sentence-transformers streamlit python-dotenv pydantic pypdf
```

### 4️⃣ Verify Setup

```bash
python check_system.py
```

This should show:
- ✅ All imports successful
- ✅ Ollama connection working
- ✅ Policy files found

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Your browser will open at: `http://localhost:8501`

### 6️⃣ Using the Application

1. Click "🚀 Initialize Agent" in the sidebar
2. Wait 30-60 seconds for first-time initialization
3. Start asking questions!

**Try these:**
- "What is the annual leave policy?"
- "How many sick leave days do I get?"
- "What about casual leave?" (follow-up)
- "How do I apply for work from home?"

---

## Troubleshooting

### "Failed to initialize agent"
```bash
# Check if Ollama is running
ollama serve

# Check if model is downloaded
ollama list

# If mistral not found:
ollama pull mistral
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific missing package:
pip install <package-name>
```

### Slow performance
```bash
# Try a smaller model
ollama pull phi

# Then select 'phi' in the Streamlit sidebar
```

### Agent gives errors
- Check that policy files exist in `data/policies/`
- Ensure Ollama service is running
- Try reinitializing the agent

---

## Testing Without UI

Run the test script:
```bash
python test_agent.py
```

This will test the agent with sample queries in the terminal.

---

## Project Structure

```
agentic/
├── app.py                  ← Main Streamlit UI
├── agent/
│   ├── hr_agent.py        ← Agent implementation
│   ├── tools.py           ← Policy retrieval tools
│   └── prompts.py         ← Agent prompts
├── data/
│   └── policies/          ← HR policy documents (3 files)
├── requirements.txt       ← Dependencies
├── test_agent.py          ← Test script
└── check_system.py        ← System verification
```

---

## Next Steps

✅ **System is ready!** You can now:

1. **Test the agent** with various HR policy questions
2. **Add custom policies** by creating new `.txt` files in `data/policies/`
3. **Customize prompts** in `agent/prompts.py`
4. **Try different models** from the Streamlit sidebar

---

## Key Features Implemented

✅ ReAct Agent Pattern (Reasoning + Acting)  
✅ Conversational Memory (context retention)  
✅ Semantic Search over policies  
✅ Local LLM (Ollama) - zero cost  
✅ Streamlit Chat UI  
✅ Follow-up question handling  
✅ Multiple policy documents  

---

**🎉 Happy Testing!**
