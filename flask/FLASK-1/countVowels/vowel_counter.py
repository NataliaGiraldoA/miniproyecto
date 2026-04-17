def vowel_counter(text) -> int:
    text = text.lower()  
    vowels = 'aeiou'   
    count = sum(letter in vowels for letter in text) 
    return count  
