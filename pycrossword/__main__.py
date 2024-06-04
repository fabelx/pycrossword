import asyncio
from argparse import ArgumentParser, Namespace

from .__version__ import __version__
from .logger import setup_logging

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

    return parser.parse_args()


async def run():
    parser = ArgumentParser(
        prog="pycrossword",
        description="A Python cli tool for generating customizable crossword puzzles.",
        add_help=False,
    )
    _ = cli(parser)

    try:
        logger.info("Done. But nothing yet!")
    except Exception as e:
        log_fatal(f"Failed due to an error: {e}")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
