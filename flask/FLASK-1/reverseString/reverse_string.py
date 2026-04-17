def reverse_string(text) -> str:
    reverse = ''
    for char in text:
        reverse = char + reverse
    return reverse