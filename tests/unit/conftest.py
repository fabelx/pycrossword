from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from pycrossword import OpenAIClient, ClueGenerator

TEST_DIR = Path(__file__).resolve().parent.parent


def get_file_path(filename: str) -> Path:
    """Get path for a file with words.

    Args:
        filename: Filename of file with words.

    Returns:
        str: Full path of file with words.
    """
    return TEST_DIR / "words" / filename


@pytest.fixture(scope='function')
def unique_words(filename: str) -> list[str]:
    filepath = get_file_path(filename=filename)
    with open(filepath, "r") as f:
        return f.read().splitlines()


@pytest.fixture(scope='function')
def words_with_duplicates(unique_words: list[str]) -> list[str]:
    return unique_words * 2


@pytest.fixture(scope='function')
def words_with_non_alpha_characters() -> list[str]:
    # words with non-alphabetic characters
    return ["hell0"]


@pytest.fixture(scope='function')
def client() -> OpenAIClient:
    return OpenAIClient(api_token="")


@pytest.fixture(scope='function')
def client_with_mock(client, content) -> OpenAIClient:
    with patch("openai.OpenAI") as mock_open_ai_client:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=content))]
        mock_open_ai_client.chat.completions.create.return_value = mock_response
        client.client = mock_open_ai_client
        yield client


@pytest.fixture(scope='function')
def clue_generator(client_with_mock) -> ClueGenerator:
    return ClueGenerator(client_with_mock, cacheable=True)
