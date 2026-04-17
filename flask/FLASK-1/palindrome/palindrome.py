def palindrome(cadena) -> bool:
    cadena = ''.join(cadena.split())

    for i in range(len(cadena) // 2):
        if cadena[i] != cadena[len(cadena) - 1 - i]:
            return False
    return True

