# RISC Assembler (`risc_assembler.py`)

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

* Type in assembly code line-by-line
* End with a blank line
* Output is shown immediately

### 🔸 Batch Mode

```bash
python risc_assembler.py program.asm -o program.hex --sym symbols.txt
```

| Option  | Description                                |
| ------- | ------------------------------------------ |
| `-o`    | Output file in Logisim hex format          |
| `--sym` | Optional symbol table (labels + addresses) |

---

## 📥 Example Input (Assembly)

```asm
SET R1, 10
SET R2, 20
ADD R3, R1, R2
SW R3, 0(R0)
```

## 📤 Example Output (Hex)

```text
v2.0 raw
001A000D 0028000D 00431000 01200011
```

---

## 👤 Authors

Assembler developed by **Mohamed Wageh Mahmoud** with **ChatGPT**, Spring 2025.
