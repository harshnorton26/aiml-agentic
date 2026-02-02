# 🏗️ System Architecture - HR Policy Assistant

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit Web App)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Chat Input   │  │  Chat History│  │   Settings   │         │
│  │              │  │   Display    │  │   Sidebar    │         │
│  └──────┬───────┘  └──────────────┘  └──────────────┘         │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                                │
│                   (LangChain ReAct Agent)                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │                  Agent Executor                  │          │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │          │
│  │  │  Reasoning │  │   Action   │  │ Observation│ │          │
│  │  │    Step    │→ │  Selection │→ │   Result   │ │          │
│  │  └────────────┘  └────────────┘  └────────────┘ │          │
│  └──────────────────────────────────────────────────┘          │
│           │                    │                                │
│           ▼                    ▼                                │
│  ┌────────────────┐   ┌────────────────────┐                   │
│  │  Conversation  │   │   Tool Selection   │                   │
│  │     Memory     │   │   & Orchestration  │                   │
│  └────────────────┘   └────────────────────┘                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        TOOLS LAYER                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Policy Retrieval Tool                    │          │
│  │                                                  │          │
│  │  ┌────────────────┐    ┌──────────────────┐    │          │
│  │  │  Query Input   │ →  │  Vector Search   │    │          │
│  │  └────────────────┘    └──────────────────┘    │          │
│  │           │                     │               │          │
│  │           │                     ▼               │          │
│  │           │            ┌──────────────────┐    │          │
│  │           │            │  FAISS Vector DB │    │          │
│  │           │            └──────────────────┘    │          │
│  │           │                     │               │          │
│  │           ▼                     ▼               │          │
│  │  ┌─────────────────────────────────────┐       │          │
│  │  │    Top-K Relevant Documents         │       │          │
│  │  └─────────────────────────────────────┘       │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Leave Policy │  │  WFH Policy  │  │ General HR   │         │
│  │   Document   │  │   Document   │  │    Policy    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌─────────────────────────────────────────────────┐           │
│  │  HuggingFace Embeddings                         │           │
│  │  (all-MiniLM-L6-v2)                             │           │
│  └─────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        LLM LAYER                                │
│                   (Local Ollama Server)                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Mistral / Llama 2 / Llama 3              │          │
│  │              (Running Locally)                   │          │
│  └──────────────────────────────────────────────────┘          │
│                  localhost:11434                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### User Query Flow

```
User Question
    │
    ▼
┌────────────────────┐
│  Streamlit Input   │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Agent Executor    │──────► Retrieve Conversation History
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ ReAct Reasoning    │
│  "Do I need tool?" │
└────────┬───────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  YES        NO
    │         │
    │         └──────► Direct Answer
    │
    ▼
┌──────────────────────┐
│  Tool: search_hr_    │
│       policy         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Semantic Search     │
│    (FAISS)           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Top 3 Relevant Docs  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  LLM Synthesis       │
│   (Ollama)           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Final Answer       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Update Memory        │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Display to User     │
└────────────────────────┘
```

---

## Component Details

### 1. User Interface (Streamlit)
**File**: `app.py`

**Responsibilities**:
- Render chat interface
- Manage user input
- Display conversation history
- Handle agent initialization
- Provide settings and controls

**Key Features**:
- Real-time chat messaging
- Example questions
- Model selection
- Conversation reset
- Status indicators

---

### 2. Agent Layer (LangChain)
**File**: `agent/hr_agent.py`

**Components**:

#### a) ReAct Agent
- **Pattern**: Reasoning + Acting
- **Process**:
  1. **Thought**: Analyze the question
  2. **Action**: Decide which tool to use (if any)
  3. **Action Input**: Formulate tool query
  4. **Observation**: Process tool result
  5. **Final Answer**: Synthesize response

#### b) Memory System
- **Type**: ConversationBufferMemory
- **Storage**: Last N messages/tokens
- **Purpose**: Context retention for follow-ups

#### c) Agent Executor
- **Max Iterations**: 5
- **Error Handling**: Graceful parsing error recovery
- **Verbose Mode**: Optional reasoning display

---

### 3. Tools Layer
**File**: `agent/tools.py`

#### Policy Retrieval Tool

**Workflow**:
```python
User Query
    ↓
Embedding Generation (HuggingFace)
    ↓
Vector Similarity Search (FAISS)
    ↓
Top-K Document Chunks (k=3)
    ↓
Formatted Response with Sources
```

**Features**:
- Semantic search (not keyword matching)
- Chunk-based retrieval (500 chars per chunk)
- Metadata tracking (source document)
- Overlap handling (50 char overlap)

---

### 4. Data Layer
**Directory**: `data/policies/`

**Policy Documents**:

1. **leave_policy.txt**
   - Annual leave (20 days)
   - Sick leave (12 days)
   - Casual leave (10 days)
   - Maternity (180 days)
   - Paternity (15 days)
   - Bereavement (3-5 days)
   - Comp off
   - Leave without pay

2. **wfh_policy.txt**
   - Eligibility criteria
   - WFH days allowed
   - Application process
   - Requirements
   - Restrictions

3. **general_hr_policy.txt**
   - Working hours
   - Public holidays
   - Attendance
   - Code of conduct
   - Performance reviews
   - Benefits

**Processing**:
- Text splitting (RecursiveCharacterTextSplitter)
- Embedding generation (all-MiniLM-L6-v2)
- Vector storage (FAISS index)

---

### 5. LLM Layer (Ollama)
**Integration**: Local server at `localhost:11434`

**Supported Models**:
- Mistral (recommended)
- Llama 2
- Llama 3
- Phi

**Configuration**:
- Temperature: 0.7 (balanced creativity/accuracy)
- Context window: Model-dependent
- Streaming: Supported
- API: Compatible with OpenAI format

---

## Memory Architecture

### Conversation Flow with Memory

```
Turn 1:
  User: "What is the annual leave policy?"
  Agent: [Retrieves policy, responds]
  Memory: Stores Q&A

Turn 2:
  User: "What about sick leave?"
  Context: [Previous Q&A] + "What about sick leave?"
  Agent: [Understands comparison context, retrieves sick leave]
  Memory: Appends new Q&A

Turn 3:
  User: "How do I apply for it?"
  Context: [All previous Q&As] + "How do I apply for it?"
  Agent: [Knows "it" = sick leave from context]
  Memory: Continues building history
```

**Memory Buffer**: 
- Stores recent conversation
- Provides context to agent
- Cleared on reset
- Max tokens: 2000 (configurable)

---

## Security & Privacy

### Local-First Architecture

```
┌─────────────────────────────────────┐
│         User's Machine              │
│                                     │
│  ┌──────────┐    ┌──────────┐      │
│  │ Streamlit│◄──►│  Agent   │      │
│  └──────────┘    └─────┬────┘      │
│                        │            │
│                        ▼            │
│                  ┌──────────┐       │
│                  │  Ollama  │       │
│                  │  (Local) │       │
│                  └──────────┘       │
│                        │            │
│                        ▼            │
│                  ┌──────────┐       │
│                  │ Policy   │       │
│                  │ Files    │       │
│                  └──────────┘       │
└─────────────────────────────────────┘

          NO EXTERNAL API CALLS
          NO DATA LEAVES MACHINE
          100% PRIVATE
```

---

## Scalability Considerations

### Current Implementation (Single User)
- ✅ Streamlit local server
- ✅ In-memory vector store
- ✅ Session-based memory

### Production Scaling (Future)
- 🔄 Multi-user support → Redis for session management
- 🔄 Persistent vector store → Chroma with PostgreSQL
- 🔄 Load balancing → Multiple Ollama instances
- 🔄 Caching → Response cache for common queries

---

## Technology Stack Details

| Layer | Technology | Purpose | Why Chosen |
|-------|-----------|---------|------------|
| **UI** | Streamlit | Web interface | Fast prototyping, Python-native |
| **Agent** | LangChain | Orchestration | Industry standard, rich ecosystem |
| **LLM** | Ollama | Inference | Local, free, private |
| **Vector DB** | FAISS | Similarity search | Fast, in-memory, CPU-efficient |
| **Embeddings** | HuggingFace | Text vectorization | Free, quality embeddings |
| **Memory** | LangChain Memory | Context retention | Built-in, simple to use |

---

## Key Design Decisions

### 1. Why ReAct vs Other Patterns?
- ✅ Transparent reasoning
- ✅ Tool usage flexibility
- ✅ Good for Q&A tasks
- ✅ Easier debugging

### 2. Why FAISS vs Chroma?
- ✅ Faster for small datasets
- ✅ In-memory operation
- ✅ No database setup needed
- ✅ CPU-only (no GPU required)

### 3. Why Ollama vs Cloud APIs?
- ✅ Zero cost
- ✅ Data privacy
- ✅ No rate limits
- ✅ Full control

### 4. Why ConversationBufferMemory?
- ✅ Simple implementation
- ✅ Exact context retention
- ✅ Good for short conversations
- ✅ No summarization needed

---

**Next**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for complete feature list and testing instructions.
