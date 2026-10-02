"""
Throwaway script for testing chunk configurations and git revert.
"""

def get_chunk_size() -> int:
    # BROKEN: Invalid chunk size 0 breaks chunking loops and causes ZeroDivisionError
    return 0

if __name__ == "__main__":
    print(f"Current chunk size: {get_chunk_size()}")
