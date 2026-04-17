def binary_search(arr, target) -> int :
    """
    Implements the binary search algorithm to find the position of a number
    in a sorted array.
    """
    position: int = -1 # Default position if the number is not found
    first: int = 0
    last = len(arr) - 1

    while first <= last and position == -1:
        middle: int = (first + last) // 2
        if arr[middle] == target:
            position = middle # Number found, update position
        elif target < arr[middle]:
            last = middle - 1 # Narrow search to the left half
        else:
            first = middle + 1 # Narrow search to the right half
    return position