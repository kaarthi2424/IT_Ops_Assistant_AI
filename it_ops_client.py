import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

async def main():
    print("Initializing IT Operations Assistant...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

    server_config = {
        "system_health": {
            "command": "python",
            "args": ["system_health_monitor.py"],
            "transport": "stdio"
        },
        "ticketing": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable-http"
        },
        "knowledge_base": {
            "command": "python",
            "args": ["knowledge_base_server.py"],
            "transport": "stdio"
        }
    }

    print("Connecting to MCP Servers...")
    client = MultiServerMCPClient(server_config)
    print("Successfully connected to all MCP Servers!")
    
    all_tools = await client.get_tools()
    print(f"Loaded {len(all_tools)} tools into the Agent's brain.")

    agent_executor = create_agent(llm, all_tools)

    system_prompt = SystemMessage(content="""You are an elite enterprise IT Operations Assistant. 
    You have access to local system metrics, remote IT support tickets, and an SOP database.
    Always think step-by-step. If you see an error or issue, automatically search the knowledge base for a resolution.""")

    print("\n==================================================")
    print(" IT Ops Assistant is active. Type 'exit' to quit.")
    print("==================================================")
    
    chat_history = [system_prompt]
    
    while True:
        user_input = input("\nYou: ").strip() 
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down agent...")
            break
        
        chat_history.append(HumanMessage(content=user_input))
        
        try:
            response = await agent_executor.ainvoke({"messages": chat_history})            
            final_content = response['messages'][-1].content
            chat_history.append(response['messages'][-1])
            
            if isinstance(final_content, list):
                clean_text = final_content[0].get('text', '')
                print(f"\nAgent:\n{clean_text}")
            else:
                print(f"\nAgent:\n{final_content}")
                
            if len(chat_history) > 21: 
                chat_history = [chat_history[0]] + chat_history[-20:]
                
        except Exception as e:
            print(f"\nAgent encountered an error: {e}")

if __name__ == "__main__":
    asyncio.run(main())