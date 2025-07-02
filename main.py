import asyncio

from a2a_client_agent import A2ATemplate

if __name__ == "__main__":
    asyncio.run(A2ATemplate.query_agent("http://localhost:5000", input()))