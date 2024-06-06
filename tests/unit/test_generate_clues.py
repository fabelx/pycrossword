import pytest

from pycrossword import ClueDifficulty
from pycrossword.clue.clue import GPT3_TURBO, ClueGenerator


def test_render_query(client):
    query = client.render_query("day", "time", ClueDifficulty.EASY)
    assert isinstance(query, str)


@pytest.mark.parametrize("content", ("The time it takes for Earth to complete one rotation.",))
def test_request(client_with_mock):
    query = client_with_mock.render_query("day", "time", ClueDifficulty.EASY)
    response = client_with_mock.request(query)
    assert response == "The time it takes for Earth to complete one rotation."
    client_with_mock.client.chat.completions.create.assert_called_once_with(
        model=GPT3_TURBO,
        messages=[{"role": "user", "content": query}],
        temperature=0.9
    )


@pytest.mark.parametrize("content", ("A single distinct meaningful element of speech or writing.",))
def test_clue_generator(clue_generator):
    clue = clue_generator.create("word")

    assert isinstance(clue, str)
    assert clue.endswith(".")


@pytest.mark.parametrize("content", ("",))
def test_clue_generator_fail(clue_generator):
    with pytest.raises(ValueError) as e:
        clue_generator.create("word")

    assert str(e.value) == "No response from the chat model."


@pytest.mark.parametrize("content", ("Some kind of clue.",))
def test_clues_generation(clue_generator):
    clues = clue_generator.create(["word", "day", "night"])
    assert isinstance(clues, dict)
    assert len(clues) == 3


@pytest.mark.parametrize("content", ("Some kind of clue.",))
def test_clue_generator_get_clue(clue_generator):
    clue_generator.create("day")
    assert len(clue_generator.clues) == 1

    words = ["word", "day", "night"]
    expected = [1, 2, 1]
    clue_generator.create(words)
    assert len(clue_generator.clues) == 3
    for word, e in zip(words, expected):
        assert isinstance(clue_generator.get(word), str)
        assert len(clue_generator.clues[word]) == e

    assert clue_generator.get("none") is None
    assert isinstance(clue_generator.clues["none"], list)


def test_non_cacheable_clue_generator_get_clue(client):
    clue_generator = ClueGenerator(client, cacheable=False)
    with pytest.raises(TypeError) as e:
        clue_generator.get("day")

    assert isinstance(clue_generator.clues["day"], list)
    assert str(e.value) == "Can't get clue from non cacheable generator."


def test_is_cacheable_clue_generator(client):
    clue_generator = ClueGenerator(client)
    assert clue_generator.is_cacheable

    clue_generator = ClueGenerator(client, cacheable=False)
    assert not clue_generator.is_cacheable
