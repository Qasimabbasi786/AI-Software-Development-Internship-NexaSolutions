"""
Throwaway script for testing chunk configurations and git revert.
"""

def get_chunk_size() -> int:
    # Standard stable chunk size for text retrieval
    return 350

if __name__ == "__main__":
    print(f"Current chunk size: {get_chunk_size()}")
