```markdown
# 32-bit RISC Pipelined CPU Project

Final project for the Spring 2025 Computer Architecture course. This repo includes a custom 32-bit RISC ISA processor implemented in Logisim, a Python-based assembler, test programs, and documentation.

---

## 🔧 Project Highlights

- ✅ Custom 32-bit instruction set architecture (ISA)
- ✅ Single-cycle and pipelined CPU versions
- ✅ Python assembler with label and immediate support
- ✅ Control unit ROM and truth table
- ✅ Thorough test programs and validation
- ⚠️ 2-bit branch predictor (bonus) – partially implemented

---

## 📁 Structure

| Folder         | Description                                     |
|----------------|-------------------------------------------------|
| `assembler/`   | Python assembler and usage guide                |
| `circuits/`    | Logisim `.circ` files for single & pipelined CPU|
| `test_programs/` | Assembly and HEX test programs                |
| `control_unit/`| Control signal truth table and ROM data         |
| `documentation/` | Project report in DOCX and PDF format         |
| `videos/`      | Links to CPU simulation demo videos             |

---

## ⚙️ Running the Assembler

```bash
cd assembler
python risc_assembler.py my_program.asm -o my_program.hex
````

Then load the `.hex` into the instruction memory of your Logisim circuit.

---

## 📜 Documentation

The project documentation (`Project Report.pdf`) covers:

* Datapath design
* Control unit signals
* Simulation results
* Testing methodology
* Forwarding, hazard detection, and branch logic

---

## 🎥 Videos

> Videos are available via Google Drive:

* [Pipelined CPU Demo](https://drive.google.com/your_demo_video)
* [Single-Cycle CPU Demo](https://drive.google.com/your_single_cycle_demo)

---

## 👥 Team Members

* **Mohamed Wageh Mahmoud (CSE)**
* **Youssef Ibrahim Mohamed (CSE)**
* **Mohamed Ahmed Kassem (ECE)**

---

## 🏁 Status

| Component        | Status      |
| ---------------- | ----------- |
| Single-cycle CPU | ✅ Completed |
| Pipelined CPU    | ✅ Completed |
| Assembler        | ✅ Working   |
| Branch Predictor | ⚠️ Partial  |

```
