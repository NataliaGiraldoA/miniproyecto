def asterisk_pyramid(limit) -> str:
    result = []  

    for i in range(1, limit + 1):
        line = ' '.join('*' for _ in range(i)) 
        result.append(line)  


    for i in range(limit, 0, -1):
        line = ' '.join('*' for _ in range(i)) 
        result.append(line)  

    return '\n'.join(result)