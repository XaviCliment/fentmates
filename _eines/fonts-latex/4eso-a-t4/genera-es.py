# Versió en castellà de genera.py: t4-fitxa-exercicis-es.tex i t4-fitxa-solucions-es.tex
# (4º ESO Matemáticas A, Unidad 4: Ecuaciones), amb la mateixa llista d'exercicis (T(va, es) amb LANG='es').
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, 'genera.py'), 'es'], check=True)
