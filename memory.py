from langchain_core.chat_history import InMemoryChatMessageHistory

chat_histories = {}

def get_chat_history(session_id):

    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()

    return chat_histories[session_id]