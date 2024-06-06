import pytest

from pycrossword import generate_crossword


@pytest.mark.parametrize("filename", ("word-set-1.txt",))
def test_generate_crossword(unique_words):
    dimensions, placed_words = generate_crossword(unique_words.copy(), seed=11)
    efficiency = (len(placed_words) / len(unique_words)) * 100

    assert dimensions == (44, 48)
    assert round(efficiency, 2) == 100.00

