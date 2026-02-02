"""
Simple HR Policy Retriever (no vector DB, no LangChain dependencies)
"""

import os
from typing import List, Dict


class PolicyRetriever:
    """Loads policy text files and returns simple keyword matches."""

    def __init__(self, policy_dir: str = "data/policies"):
        self.policy_dir = policy_dir
        self.documents: List[Dict[str, str]] = []
        self._load_policies()

    def _load_policies(self) -> None:
        """Load all policy documents into memory."""
        if not os.path.exists(self.policy_dir):
            print("Warning: Policy directory not found.")
            return

        for filename in os.listdir(self.policy_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.policy_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    self.documents.append({
                        "source": filename,
                        "content": f.read()
                    })

        if not self.documents:
            print("Warning: No policy documents found!")
        else:
            print(f"Loaded {len(self.documents)} policy documents")

    def search_policy(self, query: str, max_chars: int = 400) -> str:
        """Simple keyword search across policy docs, returning concise snippets."""
        if not self.documents:
            return "No policy documents available. Please check the data/policies directory."

        terms = [t.strip(".,?!") for t in query.lower().split() if len(t) > 2]
        scored = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            score = sum(1 for t in terms if t in content_lower)
            if score > 0:
                scored.append((score, doc))

        if not scored:
            return "No relevant policy information found."

        scored.sort(key=lambda x: x[0], reverse=True)
        top_docs = [d for _, d in scored[:2]]

        results = []
        for doc in top_docs:
            content = doc["content"]
            content_lower = content.lower()

            # Find best match position for any term
            best_pos = None
            for t in terms:
                pos = content_lower.find(t)
                if pos != -1:
                    best_pos = pos if best_pos is None else min(best_pos, pos)

            if best_pos is None:
                snippet = content[:max_chars].strip()
            else:
                start = max(best_pos - max_chars // 2, 0)
                end = min(start + max_chars, len(content))
                snippet = content[start:end].strip()

            results.append(f"[From {doc['source']}]\n{snippet}")

        return "\n\n---\n\n".join(results)


# For testing
if __name__ == "__main__":
    retriever = PolicyRetriever()
    test_queries = [
        "What is the annual leave policy?",
        "How do I apply for work from home?",
        "What are the working hours?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("="*50)
        result = retriever.search_policy(query)
        print(result)
        print("\n")
