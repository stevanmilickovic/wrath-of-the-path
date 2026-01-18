# Wrath of the Path (Python + Pygame)

Vizualna demonstracija 3 algoritma pretrage puta kroz generisani lavirint na 50x50 gridu:
- BFS
- DFS
- A*

Aplikacija:
1) Generiše lavirint (maze generator).
2) Korisnik bira algoritam.
3) Prikazuje korake pretrage (visited/frontier).
4) Nakon pronalaska puta, igrač se kreće ćeliju po ćeliju do cilja.

## Tech
- Python 3.10
- Pygame

## Run
```bash
pip install -r requirements.txt
python -m src.main