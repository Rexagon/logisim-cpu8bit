# logisim-cpu8bit
There was too boring evening, so...

8 bit logisim CPU with own assembler

## Assembler
| # | Mnemonics              | Action                       |
| - | ---------------------- | ---------------------------- |
| 0 | `AND Ra, Rb`           | `Ra &= Rb`                   |
| 1 | `OR Ra, Rb`            | `Ra \|= Rb`                  |
| 2 | `ADD Ra, Rb`           | `Ra += Rb`                   |
| 3 | `SUB Ra, Rb`           | `Ra -= Rb`                   |
| 4 | `LW Ra, (Rb)`          | `Ra = Mem[Rb]`               |
| 5 | `SW Ra, (Rb)`          | `Mem[Rb] = Ra`               |
| 6 | `MOV Ra, Rb`           | `Ra = Rb`                    |
| 7 | `INP Ra`               | `Ra = Inp`                   |
| 8 | `JEQ Ra, value\|label` | `PC = value\|label, Ra == 0` |
| 9 | `JNE Ra, value\|label` | `PC = value\|label, Ra != 0` |
| a | `JGT Ra, value\|label` | `PC = value\|label, Ra > 0`  |
| b | `JLT Ra, value\|label` | `PC = value\|label, Ra < 0`  |
| c | `LW Ra, value\|label`  | `Ra = Mem[value\|label]`     |
| d | `SW Ra, value\|label`  | `Mem[value\|label] = Ra`     |
| e | `LI Ra, value\|label`  | `Ra = value\|label`          |
| f | `JMP value\|label`     | `PC = value\|label`          |

## Registers
| ## | Name | Description                   |
| -- | ---- | ----------------------------- |
| 00 | R0   | User data                     |
| 01 | R1   | User data                     |
| 10 | R2   | User data (output pins A0-A7) |
| 11 | R3   | User data (output pins B0-B7) |