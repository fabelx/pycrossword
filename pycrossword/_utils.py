import json
import sys
from pathlib import Path


def render_crossword(placed_words: list, dimensions: list):
    grid = [["-" for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    for items in placed_words:
        # if horizontal
        if items[3]:
            for i in range(len(items[0])):
                grid[items[1]][items[2] + i] = items[0][i]
        else:
            for i in range(len(items[0])):
                grid[items[1] + i][items[2]] = items[0][i]

    return grid


def print_crossword(grid: list):
    for line in grid:
        print("\t", "  ".join(line))


def print_clues(clues: dict, placed_words: list):
    print("Clues:")
    for item in placed_words:
        print(f"({item[1]}, {item[2]}), {item[0]}: {clues[item[0]].pop()}")


def save(
    file_path: Path, as_json: bool, dimensions: list, placed_words: list, clues: dict
):
    if as_json:
        with open(file_path, "w") as f:
            json.dump(
                {
                    "dimensions": {"rows": dimensions[0], "cols": dimensions[1]},
                    "placed_words": [
                        {
                            "word": item[0],
                            "starting_position": {
                                "row": item[1],
                                "col": item[2],
                            },
                            "direction": "horizontal" if item[3] else "vertical",
                            "clue": clues[item[0]].pop(),
                        }
                        for item in placed_words
                    ],
                },
                f,
                indent=2,
            )
    else:
        grid = render_crossword(placed_words, dimensions)
        with open(file_path, "w") as sys.stdout:
            print_crossword(grid)
            print_clues(clues, placed_words)
