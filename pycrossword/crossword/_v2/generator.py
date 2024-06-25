import random
from collections import defaultdict

from ..utils import generate_score, random_state


def __place(
    word: str, crossword: dict, x, y, horizontal: bool, dimensions: list
) -> tuple:
    """Place a word onto the crossword grid.

    Args:
        word: The word to place.
        crossword: The current crossword grid.
        x: Starting x-coordinate.
        y: Starting y-coordinate.
        horizontal: True if placing horizontally, False if placing vertically.
        dimensions: List to track the crossword dimensions [min_x, max_x, min_y, max_y].

    Returns:
        tuple: Updated crossword grid and dimensions list.
    """
    if horizontal:
        for char in word:
            crossword[(x, y)] = char
            dimensions[2] = min(dimensions[2], y)
            dimensions[3] = max(dimensions[3], y)
            y += 1
    else:
        for char in word:
            crossword[(x, y)] = char
            dimensions[0] = min(dimensions[0], x)
            dimensions[1] = max(dimensions[1], x)
            x += 1

    return crossword, dimensions


def __place_first(word: str) -> tuple:
    """Initialize the crossword grid with the first word placed horizontally.

    Args:
        word: The first word to place.

    Returns:
        tuple: Initialized crossword grid and dimensions list.
    """
    crossword = defaultdict(str)
    return __place(word, crossword, 0, 0, True, [0, 0, 0, 0])


def __check_horizontal_placement(word: str, offset: int, crossword: dict, x, y) -> bool:
    """Check if placing the word horizontally is valid at the given position.

    Args:
        word: The word to place.
        offset: Offset position within the word.
        crossword: The current crossword grid.
        x: Starting x-coordinate.
        y: Starting y-coordinate.

    Returns:
        bool: True if placement is valid, False otherwise.
    """
    y -= offset

    if crossword[(x, y - 1)] != "" or crossword[(x, y + len(word))] != "":
        return False

    for i in range(len(word)):
        if i == offset:
            continue

        if crossword[(x, y + i)] != word[i] and crossword[(x, y + i)] != "":
            return False

        if crossword[(x - 1, y + i)] != "":
            return False

        if crossword[(x + 1, y + i)] != "":
            return False

    return True


def __check_vertical_placement(word: str, offset: int, crossword: dict, x, y) -> bool:
    """Check if placing the word vertically is valid at the given position.

    Args:
        word: The word to place.
        offset: Offset position within the word.
        crossword: The current crossword grid.
        x: Starting x-coordinate.
        y: Starting y-coordinate.

    Returns:
        bool: True if placement is valid, False otherwise.
    """
    x -= offset

    if crossword[(x - 1, y)] != "" or crossword[(x + len(word), y)] != "":
        return False

    for i in range(len(word)):
        if i == offset:
            continue

        if crossword[(x + i, y)] != word[i] and crossword[(x + i, y)] != "":
            return False

        if crossword[(x + i, y - 1)] != "":
            return False

        if crossword[(x + i, y + 1)] != "":
            return False

    return True


def __find_placements(word: str, offset: int, crossword: dict, x, y) -> list:
    """Find valid placements for a word at the given offset within the crossword grid.

    Args:
        word: The word to place.
        offset: Offset position within the word.
        crossword: The current crossword grid.
        x: Starting x-coordinate.
        y: Starting y-coordinate.

    Returns:
        list: List of valid start points for placing the word [(x, y, horizontal)].
    """
    start_points = []
    if __check_horizontal_placement(word, offset, crossword, x, y):
        start_points.append((x, y - offset, True))

    if __check_vertical_placement(word, offset, crossword, x, y):
        start_points.append((x - offset, y, False))

    return start_points


def __generate_crossword(
    words: list, x: int | None = None, y: int | None = None
) -> tuple:
    """Generate a crossword puzzle using the given list of words.

    Args:
        words: List of words to use for the crossword puzzle.
        x: Optional width constraint for the crossword grid. Defaults to None.
        y: Optional height constraint for the crossword grid. Defaults to None.

    Returns:
        tuple: Final crossword grid, dimensions list and placement list.
    """
    random.shuffle(words)
    word_ = words.pop(0)
    placed_words = [[word_, 0, 0, True]]
    crossword_, dimensions = __place_first(word_)
    count = 0
    while len(words) > 0 and count < len(words):
        word_ = words.pop(0)
        placements = []
        for i in range(len(word_)):
            for coords, value in crossword_.copy().items():
                if value == word_[i]:
                    placements.extend(__find_placements(word_, i, crossword_, *coords))

        best_score = 0
        best_crossword = crossword_.copy()
        best_placement = None
        best_dimensions = []
        for placement in placements:
            new_crossword, new_dimensions = __place(
                word_, crossword_.copy(), *placement, dimensions.copy()
            )

            if (
                x
                and new_dimensions[3] - new_dimensions[2] >= x
                or y
                and new_dimensions[1] - new_dimensions[0] >= y
            ):
                continue

            new_score = generate_score(new_crossword, new_dimensions)
            if new_score > best_score:
                best_score = new_score
                best_crossword = new_crossword
                best_placement = placement
                best_dimensions = new_dimensions

        if best_score > 0:
            crossword_ = best_crossword
            dimensions = best_dimensions
            placed_words.append([word_, *best_placement])
            count = 0
        else:
            words.append(word_)
            count += 1

    return crossword_, dimensions, placed_words


def generate_crossword(
    words: list, x: int | None = None, y: int | None = None, seed: int | None = None
) -> tuple:
    """Generate a crossword puzzle from the given list of words.

    Args:
        words: List of words to use for the crossword puzzle.
        x: Optional width constraint for the crossword grid. Defaults to None.
        y: Optional height constraint for the crossword grid. Defaults to None.
        seed: Random seed for reproducibility. Defaults to None.

    Returns:
        tuple: Dimension list and placement list.
    """
    if seed is not None:
        with random_state(seed):
            _, dimensions, placed_words = __generate_crossword(words, x, y)
    else:
        _, dimensions, placed_words = __generate_crossword(words, x, y)

    rows = dimensions[1] - dimensions[0] + 1
    cols = dimensions[3] - dimensions[2] + 1
    for i in range(len(placed_words)):
        placed_words[i][1] = placed_words[i][1] - dimensions[0]
        placed_words[i][2] = placed_words[i][2] - dimensions[2]

    return (rows, cols), placed_words
