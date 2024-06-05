def remove_duplicates(words: list) -> list:
    # regular set(words) produces semi-random sequence of words
    unique_words = []
    for word in words:
        if word in unique_words:
            continue

        unique_words.append(word)

    return unique_words


def prepare_words(words: list, allow_duplicates: bool = False) -> list:
    if not allow_duplicates:
        words = remove_duplicates(words)

    for i in range(len(words)):
        if not words[i].isalpha():
            raise ValueError(
                f"The word '{words[i]}' is invalid. Only alphabetic characters are permitted."
            )

        # normalize word to upper case, avoiding problems with i != I
        words[i] = words[i].upper()

    return words
