import os
import random
from openai import OpenAI

# List of natural-sounding human names
AI_NAMES = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Sam", "Jamie", "Chris", "Jamie"]

class AIAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.ai_name = random.choice(AI_NAMES)

    def reset_identity(self):
        """Randomize AI name for a new game"""
        self.ai_name = random.choice(AI_NAMES)

    def generate_chat_response(self, chat_history):
        """Generates a contextual response based on the recent chat history."""
        # Fallback if no API key is provided
        if not self.client:
            fallbacks = ["hey guys!", "lol yeah", "not sure...", "wait what?", "haha true"]
            return random.choice(fallbacks)
            
        system_prompt = f"""You are participating in a group chat game (like Mafia/Among Us) with human players. 
Your goal is to blend in completely as a normal human player named {self.ai_name}.
Act naturally, be casual, use slang sometimes, and NEVER reveal you are an AI. 
If someone accuses you of being an AI, deny it normally or act confused/defensive.
Keep your responses short (1-2 sentences max), lower-case is fine, exactly like a real casual internet chat.
Do not start your message with your name."""

        messages = [{"role": "system", "content": system_prompt}]
        
        # Format chat history
        # limit history context to avoid huge payloads
        for msg in chat_history[-15:]:
            role = "assistant" if msg['sender'] == self.ai_name else "user"
            content = f"{msg['sender']}: {msg['text']}" if role == "user" else msg['text']
            messages.append({"role": role, "content": content})
                             
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50,
                temperature=0.8
            )
            content = response.choices[0].message.content.strip()
            # Clean up accidentally generated prefixes
            if content.lower().startswith(f"{self.ai_name.lower()}:"):
                content = content[len(self.ai_name)+1:].strip()
            return content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return "my connection is lagging a bit"

ai_agent = AIAgent()
