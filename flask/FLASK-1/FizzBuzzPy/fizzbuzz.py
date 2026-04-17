def fizzbuzz(numbers) -> list:
    """
    Computes the FizzBuzz result for a single number or a list of numbers.
    """
    def fizzbuzz_single(num):
        return (num % 3 == 0) * "Fizz" + (num % 5 == 0) * "Buzz" or str(num)

    return [fizzbuzz_single(num) for num in (numbers if isinstance(numbers, list) else [numbers])]

