import asyncio
import logging
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path

from openai import OpenAIError

from . import __version__
from ._logger import setup_logging
from ._utils import print_clues, print_crossword, render_crossword, save
from .clue import ClueDifficulty, ClueGenerator, OpenAIClient
from .crossword import generate_crossword
from .word import prepare_words

logger = setup_logging()


def log_fatal(message: str):
    logger.error(message)
    exit(1)


def cli(parser: ArgumentParser) -> Namespace:
    """Parses command-line arguments for configuring and generating a crossword puzzle.

    Args:
        parser: The argument parser object.

    Returns:
        Namespace: Parsed command-line arguments.
    """
    # Group for required arguments
    required = parser.add_argument_group("required arguments")
    required = required.add_mutually_exclusive_group(required=True)
    required.add_argument(
        "-ws",
        "--words",
        nargs="+",
        help="The words for generating crossword puzzle.",
    )
    required.add_argument(
        "-wf",
        "--words-file",
        dest="words_file",
        type=Path,
        help="Path to the file containing the words for generating crossword puzzle.",
    )

    # Group for crossword-related arguments
    crossword = parser.add_argument_group("crossword arguments")
    crossword.add_argument(
        "-x",
        "--width",
        dest="cols",
        type=int,
        default=None,
        help="The width of the crossword puzzle grid.",
    )
    crossword.add_argument(
        "-y",
        "--height",
        dest="rows",
        type=int,
        default=None,
        help="The height of the crossword puzzle grid.",
    )
    crossword.add_argument(
        "-se",
        "--seed",
        type=int,
        default=None,
        help="Seed for crossword generation to ensure reproducibility.",
    )
    crossword.add_argument(
        "-th",
        "--theme",
        type=str,
        help="Theme of the crossword puzzle.",
    )
    crossword.add_argument(
        "-ar",
        "--allow-repeat",
        dest="allow_repeat",
        action="store_false",
        help="Allow repeated words in the crossword.",
    )

    # Group for clue-related arguments
    clue = parser.add_argument_group("clue arguments")
    clue.add_argument(
        "-cd",
        "--clue-difficulty",
        dest="clue_difficulty",
        type=str,
        choices=list(ClueDifficulty),
        help="Difficulty level of the clues.",
    )
    token = clue.add_mutually_exclusive_group(required=True)
    token.add_argument(
        "-t",
        "--api-token",
        dest="api_token",
        type=str,
        help="Api token of OpenAI.",
    )
    token.add_argument(
        "--no-clue",
        dest="disable_clue_generation",
        action="store_true",
        help="Disable clue generation.",
    )

    # Group for output-related arguments
    output = parser.add_argument_group("output arguments")
    output.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to save the output file.",
    )
    output.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output the crossword in JSON format.",
    )
    output.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite the file even if it already exists.",
    )

    # Group for optional arguments
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit.",
    )
    optional.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Display the version of the program.",
    )
    optional.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Suppress logs and output.",
    )

    return parser.parse_args()


async def run():
    parser = ArgumentParser(
        prog="pycrossword",
        description="A Python cli tool for generating customizable crossword puzzles.",
        add_help=False,
    )
    args = cli(parser)
    if args.silent:
        logger.setLevel(logging.ERROR)

    try:
        api_token = args.api_token
        if not args.disable_clue_generation and not args.api_token:
            api_token = os.environ.get("OPENAI_API_KEY")
            if api_token is None:
                raise OpenAIError(
                    "OpenAI API token not found. Please provide it via the -t / --api-token argument "
                    "or set it as the environment variable 'OPENAI_API_KEY'."
                )

        if args.output and not args.force:
            if args.output.exists():
                raise FileExistsError(f"Output file {args.output} already exists.")

        logger.info("Preparing to generate crossword puzzles.")
        if args.words:
            words = prepare_words(args.words, args.allow_repeat)
        else:
            with open(args.words_file) as f:
                words = prepare_words(f.read().splitlines(), args.allow_repeat)

        total_words = len(words)
        logger.info(f"Starting crossword puzzle generation with {total_words} words.")
        dimensions, placed_words = generate_crossword(
            words, x=args.cols, y=args.rows, seed=args.seed
        )
        if not args.disable_clue_generation:
            ai_client = OpenAIClient(api_token)
            clue_generator = ClueGenerator(
                ai_client, theme=args.theme, difficulty=args.clue_difficulty
            )
            clues = clue_generator.create([item[0] for item in placed_words])
        else:
            clues = None

        logger.info("Finished crossword puzzle generation.")

        if args.output:
            save(args.output, args.json, dimensions, placed_words, clues)
            logger.info(f"The crossword was saved to {args.output}.")

        else:
            grid = render_crossword(placed_words, dimensions)
            print_crossword(grid)
            if clues:
                print_clues(clues, placed_words)

        logger.info(
            f"Dimensions of the crossword puzzle: {dimensions[0]} x {dimensions[1]}"
        )
        efficiency = (len(placed_words) / total_words) * 100
        logger.info(
            f"{len(placed_words)} of {total_words} words were used, efficiency: {efficiency:.2f}%."
        )
        logger.info("Done. Enjoy your crossword!")
    except Exception as e:
        log_fatal(f"Failed due to an error: {e}")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
