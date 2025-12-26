# src/ai_processor.py
import os
from dotenv import load_dotenv
import openai
import logging
from typing import List, Dict, Any

load_dotenv()

logger = logging.getLogger(__name__)


class AIProcessor:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables; OpenAI calls will likely fail")
        else:
            openai.api_key = api_key

    def create_chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", max_tokens: int = 150, temperature: float = 0.7) -> Any:
        """Wrapper around OpenAI ChatCompletion API.

        Returns the raw response object from openai.ChatCompletion.create.
        """
        try:
            return openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
        except Exception as e:
            logger.error(f"Error calling OpenAI ChatCompletion: {e}")
            raise

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize the text into a few concise sentences suitable for slides."""
        if not text.strip():
            return ""

        prompt = f"Summarize the following text into {max_sentences} concise sentences suitable for a presentation slide:\n\nText: {text}\n\nSummary:"

        try:
            resp = self.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries for presentation slides."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            # Safe access to response content
            try:
                return resp.choices[0].message.content.strip()
            except Exception:
                return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"Error in AI summarization: {e}")
            sentences = text.split('.')
            return '. '.join(sentences[:max_sentences]) + ('.' if not text.endswith('.') else '')

    def generate_image_query(self, text: str) -> str:
        """Generate a short image search query (2-3 words) from text."""
        if not text.strip():
            return "abstract background"

        prompt = f"Generate a simple, relevant image search query (2-3 words) for: {text}"

        try:
            resp = self.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You generate concise image search queries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0.3
            )
            try:
                return resp.choices[0].message.content.strip()
            except Exception:
                return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"Error generating image query: {e}")
            return text.split()[0] if text.split() else "abstract"