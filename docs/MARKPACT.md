# Markpact files

Contracts in this repo (`markpacts/`) describe the **Docker bundle** view of desktop automation.

Canonical capability contracts live in sibling pack repos where applicable:

| File here | Implements |
|-----------|------------|
| `urirdp.contract.markpact.md` | `urirdp` pack (`rdp://`) |
| `urikvm.contract.markpact.md` | `urikvm` pack |
| `urihim.contract.markpact.md` | `urihim` pack |
| `uriocr.contract.markpact.md` | `uriocr` pack |
| `urillm-vision.contract.markpact.md` | `urillm` vision |
| `urikvm-rdp.contract.markpact.md` | bundle overlay |

Runtime: `urirdpedge` (`urisys-rdp`) composing standalone wheels.

The portal `markpact.com` stores reusable source contracts; this Docker package is one implementation.
