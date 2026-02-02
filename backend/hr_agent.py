"""
HR Policy Agent - LangChain + Ollama (Local LLM)
"""

from typing import Dict, Any
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import Tool
from backend.tools import PolicyRetriever
from backend.prompts import AGENT_SYSTEM_PROMPT


class SimpleMemory:
    """Simple conversation memory buffer."""
    
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.messages = []
    
    def add_message(self, role: str, content: str):
        """Add message to history."""
        self.messages.append({"role": role, "content": content})
        # Keep only last N turns
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]
    
    def get_history(self) -> list:
        """Get message history."""
        return self.messages
    
    def clear(self):
        """Clear all messages."""
        self.messages = []
    
    def format_for_prompt(self) -> str:
        """Format history for LLM prompt."""
        if not self.messages:
            return ""
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])


class HRPolicyAgent:
    """HR Policy Conversational Agent using LangChain + Ollama."""

    def __init__(self, model_name: str = "mistral", verbose: bool = False):
        """
        Initialize HR Policy Agent with Ollama.
        
        Args:
            model_name: Ollama model (mistral, llama2, llama3, phi)
            verbose: Show agent reasoning steps
        """
        self.model_name = model_name
        self.verbose = verbose
        
        print(f"Initializing agent with {model_name}...")
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.7,
            num_predict=256  # Limit output for faster responses
        )
        
        # Initialize memory for conversation context
        self.memory = SimpleMemory(max_turns=10)
        
        # Initialize policy retriever
        self.retriever = PolicyRetriever()
        
        print("✅ Agent initialized successfully!")
    
    def chat(self, message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: User's input message
            
        Returns:
            Agent's response
        """
        try:
            self.memory.add_message("user", message)
            
            # Search relevant policies
            policy_info = self.retriever.search_policy(message)
            
            # Build prompt with policy context
            history = self.memory.format_for_prompt()
            prompt = f"""{AGENT_SYSTEM_PROMPT}

Relevant Policy Information:
{policy_info}

Conversation History:
{history}

User: {message}
Assistant:"""
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response).strip()
            
            self.memory.add_message("assistant", response_text)
            return response_text
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Agent error: {e}")
            return error_msg
    
    def reset_memory(self):
        """Clear conversation memory."""
        self.memory.clear()
    
    def get_memory(self) -> Dict[str, Any]:
        """Get conversation history."""
        return {"chat_history": self.memory.get_history()}




def create_hr_agent(
    model_name: str = "mistral",
    verbose: bool = False
) -> HRPolicyAgent:
    """
    Factory function to create HR Policy Agent.
    
    Args:
        model_name: Ollama model name
        verbose: Show agent reasoning
        
    Returns:
        Configured HRPolicyAgent instance
    """
    return HRPolicyAgent(model_name=model_name, verbose=verbose)


# For testing
if __name__ == "__main__":
    print("Initializing HR Policy Agent...")
    agent = create_hr_agent(model_name="mistral", verbose=True)
    
    print("\nHR Policy Agent initialized!")
    print("="*60)
    
    # Test conversation
    test_queries = [
        "What is the annual leave policy?",
        "What about sick leave?",
        "How do I apply for work from home?",
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        print(f"🤖 Agent: ", end="")
        response = agent.chat(query)
        print(response)
        print("-"*60)
