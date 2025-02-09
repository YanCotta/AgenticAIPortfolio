import sys
import asyncio
from agents.task_router_agent import TaskRouterAgent

def main():
    # Sample file path passed as command line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    router = TaskRouterAgent()
    # Using synchronous execute to coordinate tasks
    result = router.execute(file_path)
    print("Task Results:")
    print(result)

if __name__ == "__main__":
    main()
