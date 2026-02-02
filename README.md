# Handson

Task Breakdown: - 1. Identify an industrial use case for designing conversational systems with a simple Al Agent using Langchain/LangGraph. (Few examples: - Customer Service/Data Analysis/Multi-Source or multi-Document QA Agent/...) a. Describe your problem statement/objective including the process where the Agentic Systems and Lanachain/LangGragh is utilised to build Conversational systems, and their key benefits. 2. Create effective prompts, react systems, and provide tools & memory to perform actions. 3. Compare the capabilities of Lang Chain/LangGraph in building Simple Agentic + Conversational Systems. 4. Develop a Streamlit Ul to showcase the user-bot interaction. 5. Test locally on your System.

# 🎯 HR Policy & Leave Conversational Assistant

## 📋 Problem Statement

Employees frequently raise repetitive queries related to HR policies such as leave entitlements, holidays, work-from-home rules, and general HR guidelines. These queries are usually answered manually by HR teams, leading to:

- **Delays** in getting responses
- **Increased workload** on HR personnel
- **Inconsistent answers** across different channels
- **Reduced productivity** as employees wait for clarifications
- **Scalability issues** as the organization grows

### The Solution

Design a **single conversational AI agent** using LangChain that can:
- Understand employee queries in natural language
- Retrieve relevant HR policy information using tools
- Maintain conversation context for follow-up questions
- Respond in a natural conversational manner
- Use a **locally deployed open-source LLM via Ollama**, ensuring **zero inference cost** and **data privacy**

---

## 🎯 Objective

Build a **Single-Agent Conversational AI System** using LangChain that:

1. **Answers HR policy questions** using natural language understanding
2. **Explains leave types** (annual, sick, casual, etc.) with policy details
3. **Handles follow-up questions** using conversation memory
4. **Decides when to use policy retrieval tools** intelligently
5. **Runs entirely locally** using Ollama for zero cost and privacy

### 🎯 Intentionally Limited Scope

To keep the implementation clean, safe, and focused, the agent has a clearly defined boundary:

---

## 🏗️ System Architecture & Approach

### Agentic System Design

This project implements a **Single-Agent Architecture** using LangChain's Agent framework:

```
Employee Query → Agent (LLM) → Tool Selection → Knowledge Retrieval → Response Generation
                     ↑                                                        ↓
                     └────────────── Conversation Memory ──────────────────────┘
```

### How LangChain Powers the System

#### 1. **Agent Layer (ReAct Pattern)**
- Uses **Reasoning + Acting (ReAct)** approach
- The agent analyzes user queries and decides which tools to use
- Dynamically selects appropriate actions based on context
- Chains multiple tool calls when needed

#### 2. **Tools & Function Calling**
The agent has access to specialized tools:
- **Policy Document Retriever**: Searches HR policy database using semantic search
- **FAQ Search Tool**: Finds relevant answers from FAQ knowledge base
- **Document QA Tool**: Performs question-answering on specific policy sections

#### 3. **Memory Management**
- **Conversation Buffer Memory**: Maintains recent conversation history
- **Context-aware responses**: Understands references like "what about casual leave?" after discussing sick leave
- **Session persistence**: Tracks user interactions throughout the conversation

#### 4. **Local LLM Integration (Ollama)**
- Runs **Llama 2/3** or **Mistral** models locally
- Ensures **data privacy** - no external API calls
- Cost-effective and customizable
- Full control over model behavior

---

## 🤖 Agent Responsibilities

### ✅ What the Agent WILL Do

1. **Answer HR Policy Questions**
   - Explain company HR policies and guidelines
   - Provide information about work-from-home rules
   - Clarify general HR procedures
   - Answer questions about holidays and working hours

2. **Explain Leave Types**
   - Describe different leave categories (annual, sick, casual, etc.)
   - Explain leave entitlements and rules
   - Provide leave policy information
   - Clarify leave application procedures

3. **Handle Follow-up Questions Using Memory**
   - Maintain conversation context across multiple turns
   - Understand references to previous questions
   - Handle pronouns and implicit context (e.g., "What about casual leave?")
   - Provide coherent multi-turn conversations

4. **Decide When to Use Policy Tools**
   - Intelligently determine when to retrieve policy documents
   - Use search tools only when necessary
   - Provide direct answers when information is already known
   - Chain tool usage when needed for complex queries

### ❌ What the Agent WILL NOT Do

1. **Approve Leaves**
   - No leave approval functionality
   - No integration with HRMS systems
   - Cannot submit leave requests on behalf of users

2. **Access Real Employee Data**
   - No access to employee databases
   - No personal information retrieval
   - No leave balance calculations for specific employees
   - Privacy-focused design

3. **Perform Workflows**
   - No multi-step business process execution
   - No automated actions or integrations
   - Information-only responses
   - (Workflows are scope for future hands-on exercises)

> **Design Philosophy**: Keep it clean, safe, and focused on conversational information retrieval

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Framework** | LangChain | Orchestrates agent, tools, and memory |
| **LLM** | Ollama (Llama 2/3/Mistral) | Local language model - **zero inference cost** |
| **Tools** | LangChain Tools | Policy retrieval, FAQ search |
| **Memory** | ConversationBufferMemory | Context retention across turns |
| **UI** | **Streamlit** | Interactive chat interface |
| **Vector Store** | FAISS/Chroma | Document embeddings for semantic search |
| **Embeddings** | HuggingFace Embeddings | Convert text to vectors locally |

**Key Technology Highlights:**
- 🔒 **100% Local Deployment**: No external API calls, full data privacy
- 💰 **Zero Inference Cost**: Ollama runs models locally for free
- ⚡ **Fast Setup**: Minimal dependencies, quick deployment

---

## ✨ Key Benefits

### For Employees
- ✅ **Instant Responses**: No waiting for HR personnel
- ✅ **24/7 Availability**: Get answers anytime
- ✅ **Consistent Information**: Same accurate answers for everyone
- ✅ **Natural Conversations**: Context-aware follow-up handling

### For HR Department
- ✅ **Reduced Workload**: Automate repetitive query handling
- ✅ **Scalability**: Handle unlimited concurrent queries
- ✅ **Focus on Strategic Work**: Free up time for complex cases

### For Organization
- ✅ **Zero Inference Cost**: No LLM API fees with Ollama
- ✅ **Data Privacy**: All processing happens locally
- ✅ **Easy Customization**: Tailored to company-specific policies
- ✅ **Quick Deployment**: Simple setup on standard hardware

---

## 🔄 LangChain vs LangGraph: Capability Comparison

### When to Use LangChain (Our Choice)

**Best for:**
- Single-agent systems with linear workflows
- Straightforward tool selection and execution
- Sequential reasoning tasks
- Quick prototyping and deployment

**Advantages:**
- ✅ Simpler implementation
- ✅ Lower learning curve
- ✅ Built-in ReAct agent patterns
- ✅ Extensive tool ecosystem
- ✅ Well-documented memory solutions

### When to Use LangGraph

**Best for:**
- Multi-agent collaboration
- Complex, cyclical workflows
- Conditional branching logic
- State machines with multiple paths
- Advanced orchestration needs

**Advantages:**
- ✅ Fine-grained control over agent flow
- ✅ Explicit state management
- ✅ Graph-based workflow visualization
- ✅ Better for complex decision trees

### Our Decision Rationale

For this **HR Policy Assistant**, LangChain is the optimal choice because:
1. Single agent is sufficient for the use case
2. Linear ReAct pattern fits the query → retrieve → respond flow
3. Simpler codebase = easier maintenance
4. Faster development and deployment

*Note: If we expand to multi-agent scenarios (e.g., HR Agent + Payroll Agent + Benefits Agent), LangGraph would become more suitable.*

---

## 📁 Project Structure

```
agentic/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app.py                    # Streamlit UI application
├── agent/
│   ├── __init__.py
│   ├── hr_agent.py          # Main agent implementation
│   ├── tools.py             # Custom tools (policy retriever, FAQ search)
│   └── prompts.py           # Agent prompts and templates
├── data/
│   ├── policies/            # HR policy documents (PDF/TXT)
│   └── faqs/                # FAQ knowledge base
├── config/
│   └── config.yaml          # Configuration (model, memory settings)
└── tests/
    └── test_agent.py        # Unit tests
```

---

## 🚀 Getting Started (Coming Soon)

### Prerequisites
- Python 3.10+
- Ollama installed locally
- 8GB+ RAM recommended

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd agentic

# Install dependencies
pip install -r requirements.txt

# Pull Ollama model
ollama pull llama2
```

### Running the Application
```bash
# Start Streamlit UI
streamlit run app.py
```

---

## 🎯 Sample Interactions

**Example 1: Direct Query**
```
User: What is the annual leave policy?
Agent: According to our HR policy, employees are entitled to 20 days of annual 
       leave per year. Leave accrues monthly at 1.67 days per month. You can 
       carry forward up to 5 unused days to the next year.
```

**Example 2: Contextual Follow-up**
```
User: How do I apply for sick leave?
Agent: To apply for sick leave, log into the HR portal, navigate to Leave 
       Management, and submit a leave request. For absences over 3 days, 
       a medical certificate is required.

User: What about casual leave?
Agent: [Understands context] Casual leave follows a similar process. You're 
       entitled to 10 days per year. No medical certificate needed, but 
       requests should be submitted at least 24 hours in advance when possible.
```

---

## 📊 Future Enhancements

- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Integration with HR management systems
- [ ] Analytics dashboard for query patterns
- [ ] Fine-tuned model on company-specific data
- [ ] Multi-agent expansion (Payroll, Benefits, Recruitment agents)

---

## 📝 License

This project is developed as part of an AI/ML hands-on assignment.

---

## 👥 Contributing

This is an educational project. Feedback and suggestions are welcome!

---

**Built with ❤️ using LangChain, Ollama, and Streamlit**


User Question: "What is the probation period?"
        ↓
    hr_agent.py receives question
        ↓
    PolicyRetriever.search_policy("What is the probation period?")
        ↓ (searches data/policies/*.txt files)
    Returns: "Probation Period: 3 months for new joiners..."
        ↓
    hr_agent.py combines:
      • AGENT_SYSTEM_PROMPT (from prompts.py)
      • Retrieved policy snippet (from tools.py)
      • User question
        ↓
    Sends to Ollama/Mistral LLM
        ↓
    Returns formatted response
        ↓
    app.py displays in Streamlit UI