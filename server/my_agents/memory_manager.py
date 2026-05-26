import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

load_dotenv()

chroma_client = chromadb.PersistentClient(path="db/chroma_db")

collection_name = "user_memory"

vector_store = Chroma(
    client=chroma_client,
    collection_name=collection_name,
    embedding_function=OpenAIEmbeddings(),
)

async def extract_and_store_memory(session_id: str):
    try:
        async with AsyncSqliteSaver.from_conn_string("db/conversations.db") as memory:
            config = {"configurable": {"thread_id": session_id}}
            checkpoint_tuple = await memory.aget_tuple(config)
            if not checkpoint_tuple:
                print(f"No checkpoint found for session {session_id}")
                return
            
            state = checkpoint_tuple.checkpoint
            
            if not state or "channel_values" not in state or "messages" not in state["channel_values"]:
                print(f"No messages found in state for session {session_id}")
                return

            messages = state["channel_values"]["messages"]
            
            if len(messages) < 2:
                return

            conversation_text = ""
            for msg in messages:
                # msg could be a dict or an object depending on Langchain version
                role = "User" if getattr(msg, "type", "") == "human" or (isinstance(msg, dict) and msg.get("type") == "human") else "Assistant"
                content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                conversation_text += f"{role}: {content}\n"

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            prompt = f"""
            Analyze the following conversation and extract any explicitly mentioned user routines, preferences, or habits.
            Focus on what the user says about themselves (e.g. "I go to the gym on Tuesdays", "I like my coffee black", "I leave for work at 8am").
            If no such information is present, output exactly: NONE
            Otherwise, output a concise bulleted list of the extracted facts.
            
            Conversation:
            {conversation_text}
            """
            
            response = await llm.ainvoke(prompt)
            extracted_text = response.content.strip()

            if extracted_text and extracted_text != "NONE":
                print(f"Extracted memory: {extracted_text}")
                vector_store.add_texts([extracted_text], metadatas=[{"session_id": session_id}])
    except Exception as e:
        print(f"Error in extract_and_store_memory: {e}")

def retrieve_user_memory(query: str):
    try:
        results = vector_store.similarity_search(query, k=3)
        if not results:
            return "No relevant user memory found."
        
        memories = [res.page_content for res in results]
        return "\n".join(memories)
    except Exception as e:
        print(f"Error in retrieve_user_memory: {e}")
        return "Error retrieving user memory."
