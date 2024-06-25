import pytest

from pycrossword import generate_crossword


@pytest.mark.parametrize("filename", ("word-set-1.txt",))
def test_generate_crossword(unique_words: list):
    dimensions, placed_words = generate_crossword(unique_words.copy(), seed=11)
    efficiency = (len(placed_words) / len(unique_words)) * 100

    assert dimensions == (44, 48)
    assert round(efficiency, 2) == 100.00


@pytest.mark.parametrize(
    "filename,width,height",
    (
        ("word-set-38-1.txt", 10, 10),
        ("word-set-38-1.txt", 30, 10),
    ),
)
def test_generate_crossword_with_dimensions(
    unique_words: list, width: int, height: int
):
    # this test is not reproducible. The generation of the crossword is random.
    dimensions, placed_words = generate_crossword(
        unique_words.copy(), x=width, y=height
    )
    x, y = dimensions

    assert x <= height
    assert y <= width
