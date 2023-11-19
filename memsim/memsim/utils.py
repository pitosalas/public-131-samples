class Block:
    def __init__(self, start: int, size: int):
        self.physical_address = start
        self.size = size

    def __str__(self):
        return f"start {pretty_mem_str(self.physical_address)}, size {pretty_mem_str(self.size)}"
    
    def contains(self, logical_address: int) -> bool:
        return logical_address <= self.size

class PageTable:
# A page table is an array, indexed by page number, that contains the frame number where that page is stored in memory.
    def __init__(self, pagesize: int):
        self.table = []
        self.frame_count = 0
        self.pagesize = pagesize
        self.size = None
    
    def add_frame(self, frame: int):
        self.table.append(frame)
        self.frame_count += 1
        self.size = self.frame_count * self.pagesize

    def __str__(self):
        return f"PageTable:  {flatten_free_segments(self.table)}"

class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping = mapping
        self.process = process

    def __str__(self):
        return f"{self.process}  {self.mapping}"

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
    multiplier = eval(info.get("multiplier"))
    return size * multiplier


def flatten_free_segments(free_segments):
    """
        Given a list of free memory segments, returns a flattened list of contiguous segments.
        chatgpt-4 improvement over my code.
        Args:
            free_segments (list): A list of integers representing free memory segments.
        Returns:
            list: A list of tuples representing contiguous memory segments.
    """
    if not free_segments:
        return []

    flattened_segments = []
    open = free_segments[0]
    previous = None

    for segment in free_segments:
        if previous is not None and segment != previous + 1:
            flattened_segments.append((open, previous))
            open = segment
        previous = segment

    flattened_segments.append((open, free_segments[-1]))
    return flattened_segments

"""
A memory manager factory, to create instances of the right kind of memory manager based on the user input.
"""
class MmFactory:
    def __init__(self) -> None:
        self.memory_manager_classes = {}

    def register(self, name, memory_manager_class):
        self.memory_manager_classes[name] = memory_manager_class

    def create(self, name):
        clazz = self.memory_manager_classes.get(name)
        if not clazz:
            raise ValueError(name)
        return clazz
    
