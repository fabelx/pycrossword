import pytest

from pycrossword import generate_crossword


def test_generate_crossword_fail():
    with pytest.raises(NotImplementedError):
        generate_crossword()
