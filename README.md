# 🧠 RISC CPU Project – Single-Cycle & Pipelined Design

This project implements a custom 32-bit RISC CPU in both **single-cycle** and **pipelined** architectures, developed as part of the Spring 2025 Computer Architecture course.

It includes:

* A custom instruction set architecture (ISA)
* Fully functional Logisim circuit implementations
* A Python-based two-pass assembler
* A test suite of assembly programs
* Bonus (partial): 2-bit branch predictor

---

## 🚀 Project Overview

* ✅ 32-bit RISC ISA with R-type, I-type, and SB-type instructions
* ✅ Single-cycle processor implemented in Logisim
* ✅ Pipelined processor with hazard detection and forwarding logic
* ✅ Python assembler to convert `.asm` to `.hex` files for Logisim
* ⚠️ Partial implementation of a 2-bit branch prediction unit (bonus)

---

## 📁 Project Structure

| Folder           | Description                                 |
| ---------------- | ------------------------------------------- |
| `assembler/`     | Contains `risc_assembler.py` and its README |
| `circuits/`      | Logisim circuit files (`.circ`)             |
| `test_programs/` | Assembly and HEX files for simulation       |
| `control_unit/`  | Control truth table and ROM file            |
| `documentation/` | Final project report in `.pdf`  |

---

## 🔁 Supported Instructions

### R-Type (Opcode 0)

* Arithmetic/Logic: `ADD`, `SUB`, `MUL`, `XOR`, `OR`, `AND`, `NOR`, `SEQ`, `SLT`, `SLTU`
* Shift Operations: `SLL`, `SRL`, `SRA`, `ROR`

### I-Type (Opcodes 1–16)

* Immediate Arithmetic: `ADDI`, `ORI`, `ANDI`, `NORI`, `XORI`, `SEQI`, `SLTI`, `SLTIU`
* Shift Immediate: `SLLI`, `SRLI`, `SRAI`, `RORI`
* Register Loading: `SET`, `SSET`, `LW`, `JALR`

### SB-Type (Opcodes 17–23)

* Memory Store: `SW`
* Branching: `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, `BGEU`

---

## 🧪 Testing

We’ve written test programs covering:

* Arithmetic/logic operations
* Memory access (`LW`/`SW`)
* Branching and jump instructions
* Label resolution and PC-relative jumps
* Array summation using procedures
* Bonus test for 2-bit branch predictor (optional)

All `.asm` files are compiled with our assembler and loaded into Logisim's memory for execution.

---

## ⚙️ How to Assemble & Simulate

### 1. Assemble Your Program

```bash
cd assembler
python risc_assembler.py my_program.asm -o my_program.hex
```

### 2. Load into Logisim

* Open a `.circ` file (e.g., `pipelined_v2.0.circ`)
* Load the `.hex` file into instruction memory
* Run the simulation

---

## 📑 Documentation

The full report is provided in `documentation/Project Report.pdf` and includes:

* Datapath and control unit diagrams
* Design of forwarding, hazard detection, and prediction logic
* Simulation screenshots and result tables
* Teamwork contributions and testing logs

---

## 👥 Team Members

* **Mohamed Wageh Mahmoud** – CSE
* **Youssef Ibrahim Mohamed** – CSE
* **Mohamed Ahmed Kassem** – ECE

---

## ✅ Project Status

| Component               | Status     |
| ----------------------- | ---------- |
| ISA + Assembler         | ✅ Complete |
| Single-Cycle CPU        | ✅ Complete |
| Pipelined CPU           | ✅ Complete |
| 2-bit Branch Predictor  | ⚠️ Partial |
| Documentation + Testing | ✅ Complete |
