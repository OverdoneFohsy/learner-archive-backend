from dotenv import load_dotenv
from google import genai

_llm_service_instance = None

class LLMService:
    def __init__(self):
        self.client = genai.Client()

    def generate_response(self, question:str, context_chunks:list, history:list):
        try:
            context_text = "\n\n".join(c['text'] for c in context_chunks)

            formatted_history = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in history])

            prompt = f"""
            You are a YouTube Video Assistant. Use the transctript snippets below to answer the question.
            If the answer is not in the transcript, say you don't have enough information.

            CONVERSATION HISTORY:
            {formatted_history if formatted_history else "No previous history."}

            PRIMARY SOURCE (Video Transcript):
            {context_text}

            SECONDARY SOURCE (Your Knowledge):
            Use your general knowledge if the primary source doesn't contain the answer.
            
            INSTRUCTIONS:
            1. If the answer is in the Transcript, prioritize it and mention "According to the video..."
            2. If the answer is NOT in the Transcript, use your own knowledge to answer the user, but add a small note that this wasn't explicitly mentioned in the video.

            USER QUESTION:
            {question}
            """

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            print(f"response: {response}")

            return response.text
        
        except Exception as e:
            print(f"Error in generating response: {e}")
            return None
    
def get_llm_service():
    global _llm_service_instance
    if not _llm_service_instance:
        _llm_service_instance = LLMService()

    return _llm_service_instance