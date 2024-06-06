import contextlib
import random
from typing import Generator


@contextlib.contextmanager
def random_state(seed: int) -> Generator:
    """Context manager to set and reset the random seed.

    Args:
        seed: Random seed.

    Yields:
        Generator: Context for the random seed.
    """
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)


def generate_score(crossword: dict, dimensions: list) -> float:
    """Generate a score for the crossword puzzle based on its size and fill ratio.

    Args:
        crossword: The crossword grid.
        dimensions: Dimensions of the crossword grid [min_x, max_x, min_y, max_y].

    Returns:
        float: Score of the crossword puzzle.
    """
    # Example:
    #   crossword grid for 2 words ["ARCO", "CO"]
    #   - - - C
    #   A R C O
    #   >>> crossword = {(-1, 3): "C", (0, 3): "O", (0, 0): "A", (0, 1): "R", (0, 2): "C"}
    #   >>> dimensions = [-1, 0, 0, 3]  # 2 rows and 4 cols
    #   >>> generate_score(crossword, dimensions)
    #   >>> 38.333..
    if dimensions[1] - dimensions[0] > dimensions[3] - dimensions[2]:
        size_ratio = (dimensions[3] - dimensions[2] + 1) / (
            dimensions[1] - dimensions[0] + 1
        )
    else:
        size_ratio = (dimensions[1] - dimensions[0] + 1) / (
            dimensions[3] - dimensions[2] + 1
        )

    area = (dimensions[1] - dimensions[0] + 1) * (dimensions[3] - dimensions[2] + 1)
    allocated = len(list(filter(None, crossword.values())))

    try:
        filled_ratio = allocated / (area - allocated)
    except ZeroDivisionError:
        filled_ratio = 0.0

    return size_ratio * 10 + filled_ratio * 20
