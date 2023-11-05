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
    
