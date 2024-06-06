import enum
import random
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import singledispatchmethod

from openai import OpenAI

GPT3_TURBO = "gpt-3.5-turbo"
GPT4_TURBO = "gpt-4-turbo-preview"


class ClueDifficulty(enum.StrEnum):
    """Enumeration for different difficulty levels of crossword clues."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class BaseClient(ABC):
    """Abstract base class for clients interacting with the service."""

    @abstractmethod
    def request(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def render_query(self, *args, **kwargs) -> str:
        raise NotImplementedError


class OpenAIClient(BaseClient):
    """Implementation of BaseClient using OpenAI API."""

    def __init__(self, api_token: str, model: str = GPT3_TURBO):
        """Initialize the OpenAIClient with an API token and model.

        Args:
            api_token: The API token for OpenAI.
            model: The model to use for generating clues.
        """
        self.client = OpenAI(api_key=api_token)
        self.model = model

    def request(self, query: str) -> str:
        """Send a request to the OpenAI API and return the response.

        Args:
            query: The query to send to the OpenAI API.

        Returns:
            str: The response from the OpenAI API.

        Raises:
            ValueError: If no response is received from the model.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": query},
            ],
            temperature=0.9,
        )
        # todo: handle possible errors (IndexError, ...)
        chat_result = response.choices[0].message.content
        if not chat_result:
            raise ValueError("No response from the chat model.")

        return chat_result.strip()

    @staticmethod
    def render_query(word: str, theme: str, difficulty: str) -> str:
        """Create a query string for generating a crossword clue.

        Args:
            word: The word for which to generate a clue.
            theme: The theme for the crossword clue.
            difficulty: The difficulty level of the crossword clue.

        Returns:
            str: The query string.
        """
        return (
            f"Generate a {difficulty} difficulty crossword clue "
            f"for the word '{word}' with a theme related to {theme}. "
            f"Output: 1 sentence with a period at the end."
        )


class ClueGenerator:
    """A class to generate crossword clues using a client."""

    __slots__ = ("client", "theme", "difficulty", "__cacheable", "__clues")

    def __init__(
        self,
        client: BaseClient,
        theme: str = "common",
        difficulty: str = ClueDifficulty.MEDIUM,
        cacheable: bool = True,
    ):
        """Initialize the ClueGenerator with a client, theme, difficulty, and cacheable flag.

        Args:
            client: The client used to interact with the service.
            theme: The theme for the crossword clues.
            difficulty: The difficulty level of the crossword clues.
            cacheable: Whether the generated clues should be cached.
        """
        self.client = client
        self.theme = theme
        self.difficulty = difficulty
        self.__cacheable = cacheable
        self.__clues = defaultdict(list)

    @property
    def is_cacheable(self) -> bool:
        """Returns whether the generator is cacheable."""
        return self.__cacheable

    @property
    def clues(self) -> dict:
        """Returns the dictionary of cached clues."""
        return self.__clues

    @singledispatchmethod
    def create(self, word: str) -> str:
        """Generate a crossword clue for a single word.

        Args:
            word: The word for which to generate a clue.

        Returns:
            str: The generated clue.
        """
        clue = self.client.request(
            self.client.render_query(word, self.theme, self.difficulty)
        )
        if self.is_cacheable:
            self.__clues[word].append(clue)

        return clue

    @create.register
    def _(self, words: list) -> dict:
        """Generate crossword clues for a list of words.

        Args:
            words: The list of words for which to generate clues.

        Returns:
            defaultdict: A dictionary with words as keys and lists of clues as values.
        """
        clues = defaultdict(list)
        for word in words:
            clues[word].append(self.create(word))

        return clues

    def get(self, word: str) -> str | None:
        """Retrieve a cached clue for a word.

        Args:
            word: The word for which to retrieve a cached clue.

        Returns:
            str | None: A cached clue if available, else None.

        Raises:
            TypeError: If the generator is not cacheable.
        """
        if not self.is_cacheable:
            raise TypeError("Can't get clue from non cacheable generator.")

        clues = self.clues[word]
        if not clues:
            return None

        return random.choice(clues)
