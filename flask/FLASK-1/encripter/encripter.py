def encripter(text) -> str:
    result = ""
    for i in range(0, len(text)):
        cadena = text[i]
        if cadena == 'a':
            result += 'ai'
        elif cadena == 'e':
            result += 'enter'
        elif cadena == 'i':
            result += 'imes'
        elif cadena == 'o':
            result += 'ober'
        elif cadena =='u':
            result += 'ufat'
        else:
            result += cadena
    return result

