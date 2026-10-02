
# CS104: CPU Simulator Portfolio Project

Simulasi CPU sederhana dengan Python untuk project portfolio Codecademy CS104 Computer Architecture.

## Fitur
- **MemoryBus**: Simulasi RAM 256 alamat, load initial value dari file
- **Cache**: Direct-mapped cache 8 block, write-through, hit/miss tracking
- **CPU**: 8 register (R0-R7, R0 hardwired 0), Program Counter, Fetch-Decode-Execute loop
- **ISA yang didukung**:
  - `ADD Rd,Rs,Rt` : Rd = Rs + Rt
  - `SUB Rd,Rs,Rt` : Rd = Rs - Rt
  - `MUL Rd,Rs,Rt` : Rd = Rs * Rt
  - `ADDI Rd,Rs,Imm` : Rd = Rs + Immediate
  - `LW Rd,Addr` : Load Word
  - `SW Rs,Addr` : Store Word
  - `BEQ Rs,Rt,Offset` : Branch if equal
  - `J Target` : Jump
  - `HALT` : Stop

## Cara Jalanin

### 1. Setup Git (Wajib untuk portfolio)
```bash
mkdir cpu-simulator
cd cpu-simulator
git init
# copy file-file ini ke folder
git add .
git commit -m "Initial commit: CPU simulator"
```

### 2. Jalankan
```bash
python main.py
# atau
python3 main.py
```

Output akan menampilkan stage FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK per cycle.

## File Input
- `instruction_input.txt` : Daftar instruksi
- `data_input.txt` : Nilai awal memory

Kamu bisa edit file tersebut untuk test program lain!

## Contoh Program Lain untuk Dicoba
Buat penjumlahan loop:
```
ADDI,R1,R0,0
ADDI,R2,R0,5
ADDI,R3,R0,1
ADD,R1,R1,R3
SUB,R2,R2,R3
BEQ,R2,R0,2
J,3
HALT
```

Project ini sudah memenuhi semua Project Objectives Codecademy.
