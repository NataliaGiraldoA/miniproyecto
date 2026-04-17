def money_to_english(amount) -> str:



    def money_to_english(n):
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        
        if n == 0:
            return "zero"

        if n < 10:
            return ones[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])
        elif n < 1000:
            return ones[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + money_to_english(n % 100))
        else:
            return "number too large"


    dollars = int(amount)
    cents = int(round((amount - dollars) * 100))
    

    dollar_words = money_to_english(dollars) + " dollar" + ("s" if dollars != 1 else "")
    cent_words = money_to_english(cents) + " cent" + ("s" if cents != 1 else "")
    

    if cents > 0:
        return f"{dollar_words} and {cent_words}"
    else:
        return dollar_words
