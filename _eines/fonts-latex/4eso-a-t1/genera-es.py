# Versió en castellà de genera.py: t1-fitxa-exercicis-es.tex i t1-fitxa-solucions-es.tex
# (4º ESO Matemáticas A, Unidad 1: Números naturales, enteros y fraccionarios), amb la mateixa llista d'exercicis.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
_sp = importlib.util.spec_from_file_location('genera', os.path.join(HERE, 'genera.py'))
g = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(g)
n = g.build(False, 'es'); g.build(True, 'es')
print(n, 'ejercicios')
