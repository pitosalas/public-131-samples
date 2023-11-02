
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

