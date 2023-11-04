class MemoryAllocation:
    def __init__(self, process, block):
        self.block = block
        self.process = process

    def __str__(self):
        return f"Proc: {self.process} has: {self.block.size/2**10} (@ phys_addr: {self.block.start/2**10}K)"


class Block:
    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __str__(self):
        return f"Block: start = {self.start/2**10}K, size = {self.size/2**20} M"

def find_and_remove(lst, n) -> list[list[int]] | None:
    """
    Finds and removes the first occurrence of a consecutive sequence of n or more integers in the given list.

    Args:
    - lst: A list of integers.
    - n: An integer representing the minimum length of the consecutive sequence to be removed.

    Returns:
    A list containing two sub-lists:
    - The first sub-list contains the consecutive sequence of integers that was removed.
    - The second sub-list contains the remaining integers in the original list after the sequence was removed.
    """
    result = [] 
    consec = 1
    prev = lst[0] - 1

    for i, num in enumerate(lst):
        if num == prev + 1:
            result.append(num)
            consec += 1
        else:
            consec = 2
            result = [num]
        
        if consec > n:
                return [result, list(set(lst)-set(result))]
        prev = num
    return None
