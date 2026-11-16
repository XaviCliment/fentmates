# Versió en castellà de genera.py: t5-fitxa-exercicis-es.tex i t5-fitxa-solucions-es.tex
# (4º ESO Matemáticas A, Unidad 5: Sistemas de ecuaciones e inecuaciones), amb la mateixa llista d'exercicis (T(va, es) amb LANG='es').
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, 'genera.py'), 'es'], check=True)
