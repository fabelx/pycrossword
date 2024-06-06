def remove_duplicates(words: list) -> list[str]:
    """Removes duplicate words from a list while maintaining the original order.

    Args:
        words: A list of words from which duplicates need to be removed.

    Returns:
        list[str]: A list of words with duplicates removed, preserving the original order.
    """
    # regular set(words) produces semi-random sequence of words
    unique_words = []
    for word in words:
        if word in unique_words:
            continue

        unique_words.append(word)

    return unique_words


def prepare_words(words: list, allow_duplicates: bool = False) -> list[str]:
    """Prepares a list of words by normalizing them to uppercase and optionally removing duplicates.

    Args:
        words: A list of words to be prepared.
        allow_duplicates: If set to False, duplicate words will be removed. Defaults to False.

    Returns:
        list[str]: A list of prepared words (normalized to uppercase and optionally deduplicated).

    Raises:
        ValueError: If a word contains non-alphabetic characters.
    """
    prepared_words = []
    for word in words:
        if not word.isalpha():
            raise ValueError(
                f"The word '{word}' is invalid. Only alphabetic characters are permitted."
            )

        # normalize words to uppercase to avoid problems with case sensitivity (e.g., 'i' vs 'I')
        prepared_words.append(word.upper())

    if not allow_duplicates:
        prepared_words = remove_duplicates(prepared_words)

    return prepared_words
