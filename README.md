# Nand to Tetris Capstone Project — Draw a Box

- **Name:** Dev Kaushik
- **Roll No:** 2501730247
- **Personal Number ($K$):** 47
- **Box Dimensions:** $64 \times 20$ pixels starting at row 47 (RAM address `17888`)
- **Assembler Extra Feature ($K \bmod 3 = 2$):** Duplicate-label warning with line number

## Repository Structure

- `NTT-CAP/CPU.hdl`, `Memory.hdl`, `Computer.hdl`: Core Hack hardware implementations (Part A).
- `NTT-CAP/SEC-A/`: Simulation screenshots verifying `CPU`, `Memory`, `ComputerAdd`, `ComputerMax`, and `ComputerRect`.
- `NTT-CAP/SEC-B/`: Two-pass Python assembler (`assembler.py`), `Box.asm`, `Box.hack`, and verification outputs/screenshots for `Max`, `Rect`, `Pong`, and duplicate-label warnings (`Dup.asm`).
- `NTT-CAP/SEC-C/`: CPU Emulator screenshot showing the black box rendered while a key is pressed.

## Usage

Assemble any Hack `.asm` program using:
```bash
python assembler.py Box.asm
