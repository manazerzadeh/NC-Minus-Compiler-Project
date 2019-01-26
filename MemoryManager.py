class MemoryManager:
    def __init__(self):
        self.dynamic_pointer = 100
        self.temp_pointer = 500

    def get_dynamic(self, dimension: int = 1):
        self.dynamic_pointer += 4 * dimension
        return self.dynamic_pointer - 4 * dimension

    def get_temp(self):
        self.temp_pointer += 4
        return self.temp_pointer - 4
