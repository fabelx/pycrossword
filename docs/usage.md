# Usage Examples
________________

> [!IMPORTANT]
> ###  For now, it's required to have the OpenAI API key set in your environment via _OPENAI_API_KEY_ or provided directly via `-t/--api-token` to the CLI tool, or as an argument during instantiation of the OpenAIClient.
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

## CLI
```bash
pycrossword -h
```
```shell
usage: pycrossword (-ws WORDS [WORDS ...] | -wf WORDS_FILE) [-se SEED] [-th THEME] [-ar] [-cd {easy,medium,hard}] [-t API_TOKEN] [-o OUTPUT] [-j] [-f] [-h] [-v] [-s]

A Python cli tool for generating customizable crossword puzzles.

required arguments:
  -ws WORDS [WORDS ...], --words WORDS [WORDS ...]
                        The words for generating crossword puzzle.
  -wf WORDS_FILE, --words-file WORDS_FILE
                        Path to the file containing the words for generating crossword puzzle.

crossword arguments:
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
Providing a seed for the reproducibility of crossword generation
```bash
pycrossword --words-file words.txt --api-token OPENAI_API_KEY
```

### Generate a crossword from a file with words and save it to a file
Providing a seed for the reproducibility of crossword generation
```bash
pycrossword --words-file words.txt --output crossword.txt --api-token OPENAI_API_KEY
```

### Generate a crossword from a file with words and save it to a file in JSON format
Providing a seed for the reproducibility of crossword generation
```bash
pycrossword --words-file words.txt --output crossword.txt --json --api-token OPENAI_API_KEY
```
