import pytest

from pycrossword import prepare_words


@pytest.mark.parametrize("filename", ("word-master-set.txt",))
def test_prepare_words(unique_words):
    prepared = prepare_words(unique_words)

    for word in prepared:
        assert word.isupper()


def test_prepare_words_with_non_alpha_characters():
    words = ["hell0"]
    with pytest.raises(ValueError) as e:
        prepare_words(words)

    assert (
        str(e.value)
        == f"The word '{words[0]}' is invalid. Only alphabetic characters are permitted."
    )
