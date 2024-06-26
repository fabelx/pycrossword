# Usage Examples
________________

> [!IMPORTANT]
> ###  It's no longer required to have the OpenAI API key set in your environment via _OPENAI_API_KEY_ or provided directly via `-t/--api-token` to the CLI tool.
________________

> [!WARNING]
> ### There are several other libraries, such as [pycrossword](https://pypi.org/project/pycrossword/) and [crossword-generator](https://pypi.org/project/crossword-generator/), which may cause conflicts if you are using them in your project.
________________

## Usage
### Create a crossword
```python
from pycrossword import generate_crossword


def main():
    words = ["amazon", "python", "night", "joy", "comprehensive"]

    # Generate the crossword puzzle using the provided words and a specific seed for reproducibility
    dimensions, placed_words = generate_crossword(words.copy(), seed=11)
    print(f"Dimensions of the crossword puzzle: {dimensions[0]} x {dimensions[1]}")

    efficiency = round((len(placed_words) / len(words)) * 100, 2)
    print(f"{len(placed_words)} of {len(words)} words were used, efficiency: {efficiency}%.")

    # Print the details of each placed word
    for word in placed_words:
        orientation = "horizontally" if word[3] else "vertically"
        print(f"{word[0]}: starting coordinate at {word[1]} x {word[2]}, placing: {orientation}.")


if __name__ == '__main__':
    main()

```

### Create a crossword puzzle with custom dimensions
```python
from pycrossword import generate_crossword


def main():
    words = ["amazon", "python", "night", "joy", "comprehensive"]

    # Generate the crossword puzzle using the provided words, a specific seed for reproducibility and dimensions
    dimensions, placed_words = generate_crossword(words.copy(), x=10, y=10, seed=11)
    print(f"Dimensions of the crossword puzzle: {dimensions[0]} x {dimensions[1]}")

    efficiency = round((len(placed_words) / len(words)) * 100, 2)
    print(f"{len(placed_words)} of {len(words)} words were used, efficiency: {efficiency}%.")

    # Print the details of each placed word
    for word in placed_words:
        orientation = "horizontally" if word[3] else "vertically"
        print(f"{word[0]}: starting coordinate at {word[1]} x {word[2]}, placing: {orientation}.")


if __name__ == '__main__':
    main()

```

### Generate clues
```python
from pycrossword import OpenAIClient, ClueGenerator, ClueDifficulty


def main():
    api_token = "Your-API-Token"
    words = ["amazon", "python", "night", "joy", "comprehensive"]
    ai_client = OpenAIClient(api_token)
    clue_generator = ClueGenerator(
        ai_client, difficulty=ClueDifficulty.MEDIUM
    )
    clues = clue_generator.create(words)
    for word, clue in clues.items():
        print(f"{word}: {"".join(clue)}")


if __name__ == '__main__':
    main()

```

## CLI
```bash
pycrossword -h
```
```shell
usage: pycrossword (-ws WORDS [WORDS ...] | -wf WORDS_FILE) [-x COLS] [-y ROWS] [-se SEED] [-th THEME] [-ar] [-cd {easy,medium,hard}] (-t API_TOKEN | --no-clue) [-o OUTPUT] [-j]
                   [-f] [-h] [-v] [-s]

A Python cli tool for generating customizable crossword puzzles.

required arguments:
  -ws WORDS [WORDS ...], --words WORDS [WORDS ...]
                        The words for generating crossword puzzle.
  -wf WORDS_FILE, --words-file WORDS_FILE
                        Path to the file containing the words for generating crossword puzzle.

crossword arguments:
  -x COLS, --width COLS
                        The width of the crossword puzzle grid.
  -y ROWS, --height ROWS
                        The height of the crossword puzzle grid.
  -se SEED, --seed SEED
                        Seed for crossword generation to ensure reproducibility.
  -th THEME, --theme THEME
                        Theme of the crossword puzzle.
  -ar, --allow-repeat   Allow repeated words in the crossword.

clue arguments:
  -cd {easy,medium,hard}, --clue-difficulty {easy,medium,hard}
                        Difficulty level of the clues.
  -t API_TOKEN, --api-token API_TOKEN
                        Api token of OpenAI.
  --no-clue             Disable clue generation.

output arguments:
  -o OUTPUT, --output OUTPUT
                        Path to save the output file.
  -j, --json            Output the crossword in JSON format.
  -f, --force           Overwrite the file even if it already exists.

optional arguments:
  -h, --help            Show this help message and exit.
  -v, --version         Display the version of the program.
  -s, --silent          Suppress logs and output.
```
___

### Generate a crossword from words
```bash
pycrossword --words amazon python night joy comprehensive --api-token OPENAI_API_KEY
```
```shell
02:06:48 Preparing to generate crossword puzzles.
02:06:48 Starting crossword puzzle generation with 5 words.
02:06:52 Finished crossword puzzle generation.
         -  -  A  -  -  -  -  -  -  -  -  -  -
         C  O  M  P  R  E  H  E  N  S  I  V  E
         -  -  A  -  -  -  -  -  I  -  -  -  -
         -  -  Z  -  -  -  -  -  G  -  -  -  -
         -  J  O  Y  -  -  -  -  H  -  -  -  -
         -  -  N  -  -  -  P  Y  T  H  O  N  -
Clues:
(1, 0), COMPREHENSIVE: This type of exam covers all topics rather than none.
(0, 2), AMAZON: The largest river in South America runs through the heart of the rainforest.
(1, 8), NIGHT: This time of day is often referred to as the opposite of day.
(4, 1), JOY: The feeling of happiness and delight.
(5, 6), PYTHON: This snake, known for its large size and powerful constriction, is not commonly found in places with very cold temperatures.
02:06:52 Dimensions of the crossword puzzle: 6 x 13
02:06:52 5 of 5 words were used, efficiency: 100.00%.
02:06:52 Done. Enjoy your crossword!
```

### Generate a crossword from words with seed
Providing a seed for the reproducibility of crossword generation
```bash
pycrossword --words amazon python night joy comprehensive --seed 11 --api-token OPENAI_API_KEY
```

### Generate a crossword from a file with words
```bash
pycrossword --words-file words.txt --api-token OPENAI_API_KEY
```

### Generate a crossword from a file with words and save it to a file
```bash
pycrossword --words-file words.txt --output crossword.txt --api-token OPENAI_API_KEY
```

### Generate a crossword from a file with words and save it to a file in JSON format
```bash
pycrossword --words-file words.txt --output crossword.txt --json --api-token OPENAI_API_KEY
```

### Generate a crossword from words without clues
Disable clue generation using the `--no-clue` flag
```bash
pycrossword --words amazon python night joy comprehensive --no-clue
```
```shell
05:56:54 Preparing to generate crossword puzzles.
05:56:54 Starting crossword puzzle generation with 5 words.
05:56:54 Finished crossword puzzle generation.
         -  -  -  -  -  -  P  -  -  -  -  -  -
         -  -  -  -  -  -  Y  -  -  -  -  -  -
         -  -  A  -  -  -  T  -  -  -  -  -  -
         C  O  M  P  R  E  H  E  N  S  I  V  E
         -  -  A  -  -  -  O  -  I  -  -  -  -
         -  -  Z  -  -  -  N  -  G  -  -  -  -
         -  J  O  Y  -  -  -  -  H  -  -  -  -
         -  -  N  -  -  -  -  -  T  -  -  -  -
05:56:54 Dimensions of the crossword puzzle: 8 x 13
05:56:54 5 of 5 words were used, efficiency: 100.00%.
05:56:54 Done. Enjoy your crossword!
```

### Generate a crossword from a file containing words, without clues, and with custom width and height (columns, rows)
Disable clue generation using the `--no-clue` flag and add `--width` / `--height`
```bash
pycrossword -wf .\tests\words\word-set-38-1.txt --no-clue --seed 11 --width 10 --height 10
```
```shell
08:44:47 Preparing to generate crossword puzzles.
08:44:47 Starting crossword puzzle generation with 38 words.
08:44:47 Finished crossword puzzle generation.
         -  S  U  S  P  E  N  D  -  -
         -  N  -  -  -  -  -  -  -  -
         T  E  R  R  I  F  I  C  -  -
         -  A  -  -  -  -  -  H  -  -
         -  K  -  -  U  -  T  E  S  T
         -  Y  A  W  N  -  -  E  -  -
         -  -  -  -  E  -  G  R  A  B
         -  -  -  -  V  -  -  -  -  -
         -  S  I  D  E  -  -  -  -  -
         -  -  -  -  N  -  -  -  -  -
08:44:47 Dimensions of the crossword puzzle: 10 x 10
08:44:47 9 of 38 words were used, efficiency: 23.68%.
08:44:47 Done. Enjoy your crossword!
```

### Generate a crossword from a file containing words, without clues, and with custom height only (rows)
Disable clue generation using the `--no-clue` flag and add only `--height`
```bash
pycrossword -wf .\tests\words\word-set-38-1.txt --no-clue --seed 11 --height 10
```
```shell
08:45:24 Preparing to generate crossword puzzles.
08:45:24 Starting crossword puzzle generation with 38 words.
08:45:24 Finished crossword puzzle generation.
         -  S  U  S  P  E  N  D  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  L  U  M  P  Y
         -  N  -  -  -  -  -  -  -  -  T  E  S  T  -  -  -  -  -  -  -  -  -  -  -  -  F  L  A  G  R  A  N  T  -  -  -  -  O  -  -
         T  E  R  R  I  F  I  C  -  -  A  -  -  -  -  -  -  B  U  S  I  N  E  S  S  -  -  -  -  -  -  D  -  -  -  -  G  -  V  -  -
         -  A  -  -  -  -  -  H  -  -  L  A  C  K  I  N  G  -  -  -  -  -  -  P  -  -  -  -  B  L  E  A  C  H  -  P  O  K  E  -  -
         -  K  -  -  U  -  L  E  V  E  L  -  -  -  -  -  R  -  -  -  -  B  -  O  -  -  H  -  -  -  -  P  -  -  -  -  V  -  -  -  -
         -  Y  A  W  N  -  -  E  -  -  -  -  -  -  -  -  E  -  -  -  -  A  -  O  -  -  U  -  D  U  S  T  Y  -  -  -  E  -  -  -  -
         -  -  -  -  E  -  B  R  A  W  N  Y  -  H  A  R  A  S  S  -  A  B  U  N  D  A  N  T  -  -  -  A  -  -  -  -  R  -  -  -  -
         -  -  -  -  V  -  -  -  -  -  -  A  -  -  -  -  S  -  -  -  -  I  -  -  -  -  G  -  -  -  -  B  O  I  L  I  N  G  -  -  -
         -  S  I  D  E  -  -  -  -  -  G  R  A  B  -  B  E  W  I  L  D  E  R  E  D  -  R  A  C  I  A  L  -  -  -  -  O  -  -  -  -
         -  -  -  -  N  -  -  -  -  -  -  N  -  -  -  -  -  -  -  -  -  S  -  -  -  -  Y  -  -  -  -  E  -  -  F  A  R  M  -  -  -
08:45:24 Dimensions of the crossword puzzle: 41 x 10
08:45:24 33 of 38 words were used, efficiency: 86.84%.
08:45:24 Done. Enjoy your crossword!
```
