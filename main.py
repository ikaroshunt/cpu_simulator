
from cpu import MemoryBus, Cache, CPU

def main():
    print("CS104 CPU Simulator - Portfolio Project\n")
    mem_bus = MemoryBus(size=256)
    mem_bus.load_from_file("data_input.txt")
    
    cache = Cache(mem_bus, cache_size=8)
    cpu = CPU(mem_bus, cache)
    cpu.load_instructions("instruction_input.txt")
    
    cpu.run()

if __name__ == "__main__":
    main()
