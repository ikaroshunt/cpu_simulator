
"""
CPU Simulator - CS104 Portfolio Project
Simulates CPU, MemoryBus, and simple Cache
ISA: ADD, SUB, MUL, ADDI, LW, SW, BEQ, J, HALT
Format: INSTRUCTION,ARG1,ARG2,ARG3 (comma separated)
"""
from collections import OrderedDict

class MemoryBus:
    def __init__(self, size=256):
        self.size = size
        self.memory = {i: 0 for i in range(size)}
    
    def load_from_file(self, filepath):
        print(f"[MemoryBus] Loading initial values from {filepath}")
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line=line.strip()
                    if not line or line.startswith("#"): continue
                    addr, val = line.split(",")
                    addr, val = int(addr.strip()), int(val.strip())
                    if 0 <= addr < self.size:
                        self.memory[addr] = val
                        print(f"  -> MEM[{addr}] = {val}")
        except FileNotFoundError:
            print(f"  ! File {filepath} not found, using zero-initialized memory")

    def read(self, address):
        if 0 <= address < self.size:
            return self.memory[address]
        raise IndexError(f"Memory address {address} out of bounds")
    
    def write(self, address, value):
        if 0 <= address < self.size:
            self.memory[address] = value
        else:
            raise IndexError(f"Memory address {address} out of bounds")

class Cache:
    """Simple direct-mapped cache with write-through"""
    def __init__(self, memory_bus, cache_size=8):
        self.memory_bus = memory_bus
        self.cache_size = cache_size
        self.cache = {}  # block -> (address, value)
        self.hits = 0
        self.misses = 0

    def read(self, address):
        block = address % self.cache_size
        if block in self.cache and self.cache[block][0] == address:
            self.hits += 1
            print(f"    [Cache] HIT for address {address}")
            return self.cache[block][1]
        else:
            self.misses += 1
            print(f"    [Cache] MISS for address {address}")
            val = self.memory_bus.read(address)
            self.cache[block] = (address, val)
            return val

    def write(self, address, value):
        block = address % self.cache_size
        self.cache[block] = (address, value)
        self.memory_bus.write(address, value)

    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits/total*100) if total else 0
        return f"Cache Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {hit_rate:.1f}%"

class CPU:
    def __init__(self, memory_bus, cache=None):
        self.memory_bus = memory_bus
        self.cache = cache if cache else Cache(memory_bus)
        self.registers = {f"R{i}": 0 for i in range(8)}  # R0-R7, R0 hardwired to 0
        self.PC = 0
        self.instructions = []
        self.halted = False
        self.cycle = 0

    def load_instructions(self, filepath):
        print(f"[CPU] Loading instructions from {filepath}")
        with open(filepath, 'r') as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#"): continue
                self.instructions.append(line)
                print(f"  -> [{len(self.instructions)-1}] {line}")
        print(f"[CPU] {len(self.instructions)} instructions loaded\n")

    def fetch(self):
        if self.PC < len(self.instructions):
            instr = self.instructions[self.PC]
            print(f"[FETCH] PC={self.PC} | {instr}")
            return instr
        return None

    def decode_execute(self, raw_instr):
        parts = [p.strip() for p in raw_instr.split(",")]
        op = parts[0].upper()
        print(f"[DECODE] Operation: {op}, Args: {parts[1:]}")

        # EXECUTE
        if op == "ADD":
            rd, rs, rt = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs] + self.registers[rt]
            print(f"[EXECUTE] {rd} = {rs}({self.registers[rs]}) + {rt}({self.registers[rt]}) = {self.registers[rd]}")
        elif op == "SUB":
            rd, rs, rt = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs] - self.registers[rt]
            print(f"[EXECUTE] {rd} = {rs} - {rt} = {self.registers[rd]}")
        elif op == "MUL":
            rd, rs, rt = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs] * self.registers[rt]
            print(f"[EXECUTE] {rd} = {rs} * {rt} = {self.registers[rd]}")
        elif op == "ADDI":
            rd, rs, imm = parts[1], parts[2], int(parts[3])
            self.registers[rd] = self.registers[rs] + imm
            print(f"[EXECUTE] {rd} = {rs}({self.registers[rs]}) + {imm} = {self.registers[rd]}")
        elif op == "LW":
            rd, addr = parts[1], int(parts[2])
            val = self.cache.read(addr)
            self.registers[rd] = val
            print(f"[MEMORY] LW {rd} <- MEM[{addr}] = {val}")
        elif op == "SW":
            rs, addr = parts[1], int(parts[2])
            self.cache.write(addr, self.registers[rs])
            print(f"[MEMORY] SW MEM[{addr}] <- {rs} = {self.registers[rs]}")
        elif op == "BEQ":
            rs, rt, offset = parts[1], parts[2], int(parts[3])
            if self.registers[rs] == self.registers[rt]:
                print(f"[BRANCH] {rs} == {rt}, branching PC {self.PC} -> {self.PC + offset}")
                self.PC += offset
                return True  # skip PC increment
            else:
                print(f"[BRANCH] {rs} != {rt}, no branch")
        elif op == "J":
            target = int(parts[1])
            print(f"[JUMP] Jumping to {target}")
            self.PC = target
            return True
        elif op == "HALT":
            print(f"[HALT] Halting CPU")
            self.halted = True
        else:
            print(f"[!] Unknown instruction {op}")

        # R0 is always 0 (MIPS convention)
        self.registers["R0"] = 0
        return False

    def run(self):
        print("\n" + "="*50)
        print("STARTING CPU SIMULATION")
        print("="*50+"\n")
        while not self.halted and self.PC < len(self.instructions):
            self.cycle += 1
            print(f"\n--- Cycle {self.cycle} ---")
            instr = self.fetch()
            if instr is None:
                break
            jumped = self.decode_execute(instr)
            if not jumped:
                self.PC += 1
            print(f"[WRITEBACK] Registers: {self.registers}")
        
        print("\n" + "="*50)
        print("SIMULATION FINISHED")
        print("="*50)
        print(f"Total Cycles: {self.cycle}")
        print(f"Final Registers: {self.registers}")
        print(f"Final PC: {self.PC}")
        print(self.cache.stats())
        print("\nMemory Dump (first 20 addresses):")
        for i in range(20):
            print(f"  MEM[{i}] = {self.memory_bus.read(i)}")
