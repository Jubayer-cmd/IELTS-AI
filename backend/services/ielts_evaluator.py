# Basic IELTS chat service

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables from .env file
load_dotenv()

class IELTSEvaluator:
    def __init__(self):
        self.llm = self._get_llm()
        
    def _get_llm(self):
        """Get Gemini LLM instance"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found. Using mock mode.")
            return None
        
        try:
            return ChatGoogleGenerativeAI(
                model='gemini-2.0-flash',
                temperature=0.7,
                google_api_key=api_key
            )
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini: {e}")
            return None
    
    async def chat(self, message: str) -> str:
        """Simple chat function"""
        try:
            system_prompt = """You are an IELTS Writing Expert AI Assistant. You help students with IELTS writing questions and provide helpful advice. Be encouraging, professional, and provide actionable advice."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            return f'Error: {str(e)}'