import enum
from collections import defaultdict

from openai import OpenAI

GPT3_TURBO = "gpt-3.5-turbo"
GPT4_TURBO = "gpt-4-turbo-preview"


class ClueDifficulty(enum.StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AIClient:

    def __init__(self, api_token: str, model: str = GPT3_TURBO):
        self.client = OpenAI(api_key=api_token)
        self.model = model

    def send_request(self, query: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": query},
            ],
            temperature=0.9,
        )
        chat_result = response.choices[0].message.content
        if not chat_result:
            raise ValueError("No response from the chat model.")

        return chat_result.strip()


class ClueGenerator:
    def __init__(
        self,
        ai_client: AIClient,
        theme: str = "common",
        difficulty: str = ClueDifficulty.MEDIUM,
    ):
        self.ai_client = ai_client
        self.theme = theme
        self.difficulty = difficulty

    def create_clue(self, word: str) -> str:
        return self.ai_client.send_request(self.render_query(word))

    def create_clues(self, words: list) -> dict:
        clues = defaultdict(list)
        for word in words:
            clues[word].append(self.create_clue(word))

        return clues

    def render_query(self, word: str) -> str:
        return (
            f"Generate a {self.difficulty} difficulty crossword clue "
            f"for the word '{word}' with a theme related to {self.theme}. "
            f"Output: 1 sentence with a period at the end."
        )
