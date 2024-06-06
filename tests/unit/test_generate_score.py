from pycrossword.crossword import generate_score


def test_generate_score():
    crossword = {(-1, 3): "C", (0, 3): "O", (0, 0): "A", (0, 1): "R", (0, 2): "C"}
    dimensions = [-1, 0, 0, 3]
    score = generate_score(crossword, dimensions)
    assert round(score, 5) == 38.33333
