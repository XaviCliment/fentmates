# Versió en castellà de la fitxa de la unitat 4 (2n ESO: Equacions de 1r i 2n grau).
# Tot el text és a genera.py, en les dues llengües (T(valencià, castellà)): aquest fitxer només l'executa amb FM_LANG=es.
# Ús: python3 genera-es.py && pdflatex t4-fitxa-exercicis-es.tex (dues vegades) && pdflatex t4-fitxa-solucions-es.tex (dues vegades)
import os, runpy
os.environ['FM_LANG'] = 'es'
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'genera.py'), run_name='__main__')
