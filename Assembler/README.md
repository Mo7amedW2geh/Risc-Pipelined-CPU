# RISC Assembler Documentation (`risc_assembler.py`)

This is a custom two-pass assembler for our 32-bit RISC ISA, used in the Spring 2025 CPU project.

It converts human-readable assembly `.asm` files into hexadecimal `.hex` files compatible with Logisim's memory format.

---

## 🚀 Features

- Supports R-type, I-type, and SB-type instructions
- Supports labels for branches and jump targets
- Allows decimal and hex immediates (e.g., `10`, `0xFF`)
- Allows comments with `;` or `#`
- PC-relative branching logic included
- Two input formats supported for `LW` and `SW`:
  - `LW R1, R2, 4`  
  - `LW R1, 4(R2)`

---

## 🛠️ Usage

### 🔸 Interactive Mode

```bash
python risc_assembler.py
```

* Enter assembly instructions line-by-line.
* Submit a blank line to finish and see the generated hex.

### 🔸 Batch Mode

```bash
python risc_assembler.py input.asm -o output.hex --sym symbols.txt
```

* `input.asm`: Your assembly source file
* `-o output.hex`: Output file for the machine code (hex)
* `--sym symbols.txt`: Optional file to save label-symbol mappings

---

## Instruction Formats

### R-Type (Opcode = 0)

```asm
MNEMONIC Rd, Rs1, Rs2
```

Example:

```asm
ADD R1, R2, R3
```

### I-Type (Opcodes 1–16)

```asm
MNEMONIC Rd, Rs1, immediate
```

Examples:

```asm
ADDI R1, R2, 10
SET R3, 0x1234
```

### Memory Instructions

#### `LW` (Load Word)

```asm
LW Rd, Rs1, imm    ; Standard format
LW Rd, imm(Rs1)    ; MIPS-style format
```

* `Rd`: Register to load into
* `Rs1`: Base address register
* `imm`: Offset

#### `SW` (Store Word)

```asm
SW Rs1, Rs2, imm   ; Standard format
SW Rs2, imm(Rs1)   ; MIPS-style format
```

* `Rs1`: Base address register
* `Rs2`: Register to store from
* `imm`: Offset

### Branch Instructions (SB-Type)

```asm
BEQ R1, R2, label
```

* Automatically calculates PC-relative offset from label

---

## Supported Instructions

### R-Type (Opcode 0)

* Arithmetic/Logic: `ADD`, `SUB`, `MUL`, `XOR`, `OR`, `AND`, `NOR`, `SEQ`, `SLT`, `SLTU`
* Shifts: `SLL`, `SRL`, `SRA`, `ROR`

### I-Type (Opcodes 1–16)

* Immediate operations: `ADDI`, `ORI`, `ANDI`, `NORI`, `XORI`, `SEQI`, `SLTI`, `SLTIU`
* Shifts with immediate: `SLLI`, `SRLI`, `SRAI`, `RORI`
* Constants: `SET`, `SSET`
* Load/jump: `LW`, `JALR`

### SB-Type (Opcodes 17–23)

* Store: `SW`
* Branches: `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, `BGEU`

---

## Output Format

```
v2.0 raw
<hex values>
```

* Compatible with Logisim’s memory file format

---

## Labels

* Labels must end with a colon and appear on their own line.

```asm
loop:
  ADD R1, R1, R2
  BNE R1, R3, loop
```

---

## Syntax Notes

* Comments start with `;` or `#`
* Immediate values can be decimal or hexadecimal (e.g. `0x10`)
* Registers must be named `R0`–`R31`
* `R0` is hardwired to zero (constant zero)

---

## 📥 Example Program

```asm
SET R1, 10
SET R2, 20
ADD R3, R1, R2
SET R4, 100
SW R4, R3, 0
LW R5, R4, 0
BEQ R3, R5, equal
SET R6, 99
equal:
SET R6, 42
BEQ R0, R0, -1
```
## Output

```
v2.0 raw
000A004D 0014008D 008208C0 0064010D 00032011 00002150 00051892 0063018D
002A018D FFE007D2
```

---

## 👤 Author

Assembler developed for Spring 2025 RISC CPU project by Mohamed Wageh with ChatGPT.

