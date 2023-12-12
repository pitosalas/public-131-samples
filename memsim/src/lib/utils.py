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
            return [result, list(set(lst) - set(result))]
        prev = num
    return None


def pretty_mem_str(size: int) -> str:
    if size < 2**10:
        return f"{size:2}"
    elif size < 2**20:
        return f"{size/2**10:.1f} KB"
    elif size < 2**30:
        return f"{size/2**20:.1f} MB"
    else:
        return f"{size/2**30:.1f} GB"


def convert_size_with_multiplier(info: dict) -> int:
    size = info["size"]
    multiplier = eval(str(info.get("multiplier")))
    return size * multiplier


def collapse_contiguous_ranges(a_list: list):
    """
    Given a list of free memory segments, returns a flattened list of contiguous segments.
    chatgpt-4 improvement over my code.
    Args:
        free_segments (list): A list of integers representing free memory segments.
    Returns:
        list: A list of tuples representing contiguous memory segments.
    """
    if not a_list:
        return []

    ranges = []
    open_range = a_list[0]
    previous = None

    for entry in a_list:
        if previous is not None and entry != previous + 1:
            ranges.append((open_range, previous))
            open_range = entry
        previous = entry

    ranges.append((open_range, a_list[-1]))
    return ranges


def check_number_in_range(number, range):
    if range == []:
        return True
    return any(number >= pair[0] and number <= pair[1] for pair in range)

def find_free_block(size, free_list):
    return next((block for block in free_list if block.size >= size), None)

def find_free_sequence(lst, target, n):  # sourcery skip: use-next
    start_of_sequence = None
    for i in range(len(lst)):
        if all(x is target for x in lst[i:i+n]): 
            start_of_sequence = i
            break
    if start_of_sequence is None:
        return None
    return(start_of_sequence, start_of_sequence+n)

def set_sequence(lst: list[None|str], first_last: set[int], process: str):
    for i in range(first_last[0], first_last[1]):
        lst[i] = process
        
