import pytest

from pycrossword import remove_duplicates


@pytest.mark.parametrize("filename", ("word-master-set.txt",))
def test_remove_duplicates(words_with_duplicates):
    unique = remove_duplicates(words_with_duplicates)

    assert len(unique) == len(set(unique))


@pytest.mark.parametrize("filename", ("word-master-set.txt",))
def test_remove_duplicates_and_check_order(unique_words):
    unique = remove_duplicates(unique_words)

    assert len(unique) == len(set(unique))
    assert unique_words == unique
