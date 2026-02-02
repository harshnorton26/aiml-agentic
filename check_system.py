"""
Simple standalone test to verify basic functionality
"""

def test_imports():
    """Test if all imports work."""
    print("Testing imports...")
    
    try:
        import langchain
        print("✅ langchain")
    except ImportError as e:
        print(f"❌ langchain: {e}")
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
    
    try:
        import ollama
        print("✅ ollama")
    except ImportError as e:
        print(f"❌ ollama: {e}")
    
    try:
        import faiss
        print("✅ faiss")
    except ImportError as e:
        print(f"❌ faiss: {e}")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers")
    except ImportError as e:
        print(f"❌ sentence-transformers: {e}")
    
    print("\n✅ Import test completed!")

def test_ollama_connection():
    """Test Ollama connection."""
    print("\nTesting Ollama connection...")
    
    try:
        import ollama
        # Try to list models
        models = ollama.list()
        print(f"✅ Connected to Ollama")
        print(f"   Available models: {[m['name'] for m in models.get('models', [])]}")
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Make sure Ollama is running: ollama serve")

def test_policy_files():
    """Test if policy files exist."""
    print("\nTesting policy files...")
    
    import os
    policy_dir = "data/policies"
    
    if os.path.exists(policy_dir):
        files = [f for f in os.listdir(policy_dir) if f.endswith('.txt')]
        print(f"✅ Found {len(files)} policy files:")
        for f in files:
            print(f"   - {f}")
    else:
        print(f"❌ Policy directory not found: {policy_dir}")

if __name__ == "__main__":
    print("="*60)
    print("HR POLICY ASSISTANT - SYSTEM CHECK")
    print("="*60)
    
    test_imports()
    test_ollama_connection()
    test_policy_files()
    
    print("\n" + "="*60)
    print("System check complete!")
    print("="*60)
