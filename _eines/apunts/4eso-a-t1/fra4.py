# Apartats 1.5-1.8 (fraccions) dels apunts de la Unitat 1 de 4t ESO A.
# La teoria, els ginys i bona part dels problemes són els dels apartats 2.5, 2.7, 2.8, 2.10 i 2.11 de 2n ESO
# (../2eso-t2/fra.py i pot.py), que s'importen tal qual; ací s'hi afigen la introducció i problemes nous d'aplicació.
# Les asserts ck() comproven els resultats escrits a mà.
from eines4a import *
import fra as F2, pot as P2

# ============================================================ 1.5 Fraccions. Fraccions equivalents
s5 = note(r"Les fraccions apareixen contínuament en els oficis: una canonada de \(\frac{3}{4}\) de polzada, \(\frac{1}{2}\) kg de farina, un descompte d'\(\frac{1}{3}\), \(\frac{2}{5}\) de la plantilla…",
          r"Las fracciones aparecen continuamente en los oficios: una tubería de \(\frac{3}{4}\) de pulgada, \(\frac{1}{2}\) kg de harina, un descuento de \(\frac{1}{3}\), \(\frac{2}{5}\) de la plantilla…",
          r"Fractions turn up all the time at work: a \(\frac{3}{4}\)-inch pipe, \(\frac{1}{2}\) kg of flour, a \(\frac{1}{3}\) discount, \(\frac{2}{5}\) of the staff…", '🔧')
s5 += F2.s5

# ============================================================ 1.6 Operacions amb fraccions
s6 = F2.s7 + F2.s8

# ============================================================ 1.7 Operacions combinades amb fraccions
s7 = note(r"En aquestes operacions apareixen alguns quadrats de fraccions: s'eleven el numerador i el denominador, \(\left(\frac{2}{3}\right)^2=\frac{2^2}{3^2}=\frac{4}{9}\). Les potències de fraccions les estudiarem amb calma a l'apartat 1.9.",
          r"En estas operaciones aparecen algunos cuadrados de fracciones: se elevan el numerador y el denominador, \(\left(\frac{2}{3}\right)^2=\frac{2^2}{3^2}=\frac{4}{9}\). Las potencias de fracciones las estudiaremos con calma en el apartado 1.9.",
          r"Some squares of fractions appear here: raise the numerator and the denominator, \(\left(\frac{2}{3}\right)^2=\frac{2^2}{3^2}=\frac{4}{9}\). We'll study powers of fractions properly in section 1.9.")
s7 += P2.s10

# ============================================================ 1.8 Problemes amb fraccions
s8 = P2.s11
s8 += sub('Problemes d’aplicació', 'Problemas de aplicación', 'Applied problems')
s8 += level(2, 7,
  prob(L(r"Una recepta de pa per a 12 persones porta \(\frac{3}{4}\) kg de farina. Quanta farina cal per a 8 persones?", r"Una receta de pan para 12 personas lleva \(\frac{3}{4}\) kg de harina. ¿Cuánta harina hace falta para 8 personas?", r"A bread recipe for 12 people uses \(\frac{3}{4}\) kg of flour. How much flour is needed for 8 people?"),
       P(r"8 persones són \(\frac{8}{12}=\frac{2}{3}\) de la recepta:", r"8 personas son \(\frac{8}{12}=\frac{2}{3}\) de la receta:", r"8 people is \(\frac{8}{12}=\frac{2}{3}\) of the recipe:"),
       r'\[\frac{2}{3}\cdot\frac{3}{4}=\frac{6}{12}=\boxed{\frac{1}{2}\ \text{kg}}\]'),
  prob(L(r"Un electricista té un rotllo de 60 m de cable. En una obra en gasta \(\frac{2}{5}\) i en una altra, \(\frac{1}{4}\) del rotllo. Quants metres li queden? Quina fracció del rotllo és?", r"Un electricista tiene un rollo de 60 m de cable. En una obra gasta \(\frac{2}{5}\) y en otra, \(\frac{1}{4}\) del rollo. ¿Cuántos metros le quedan? ¿Qué fracción del rollo es?", r"An electrician has a 60 m reel of cable. One job uses \(\frac{2}{5}\) of it and another \(\frac{1}{4}\) of the reel. How many metres are left? What fraction of the reel is that?"),
       r'\[\frac{2}{5}+\frac{1}{4}=\frac{8}{20}+\frac{5}{20}=\frac{13}{20}\qquad 1-\frac{13}{20}=\boxed{\frac{7}{20}}\]',
       r'\[\frac{7}{20}\cdot60=\frac{420}{20}=\boxed{21\ \text{m}}\]'))
ck(Fr(8, 12) * Fr(3, 4), Fr(1, 2)); ck(1 - Fr(2, 5) - Fr(1, 4), Fr(7, 20)); ck(Fr(7, 20) * 60, 21)
s8 += level(3, 9,
  prob(L(r"Un pintor fa \(\frac{1}{3}\) d'una façana el dilluns i \(\frac{3}{8}\) del que queda el dimarts. Encara li queden 50 m² per pintar. Quants metres quadrats té la façana?", r"Un pintor hace \(\frac{1}{3}\) de una fachada el lunes y \(\frac{3}{8}\) de lo que queda el martes. Todavía le quedan 50 m² por pintar. ¿Cuántos metros cuadrados tiene la fachada?", r"A painter does \(\frac{1}{3}\) of a façade on Monday and \(\frac{3}{8}\) of the rest on Tuesday. There are still 50 m² left to paint. How big is the façade?"),
       P(r"Després del dilluns queden \(\frac{2}{3}\). El dimarts en pinta \(\frac{3}{8}\cdot\frac{2}{3}=\frac{1}{4}\). En total ha pintat \(\frac{1}{3}+\frac{1}{4}=\frac{7}{12}\): queden \(\frac{5}{12}\) de la façana.", r"Después del lunes quedan \(\frac{2}{3}\). El martes pinta \(\frac{3}{8}\cdot\frac{2}{3}=\frac{1}{4}\). En total ha pintado \(\frac{1}{3}+\frac{1}{4}=\frac{7}{12}\): quedan \(\frac{5}{12}\) de la fachada.", r"After Monday \(\frac{2}{3}\) is left. On Tuesday he paints \(\frac{3}{8}\cdot\frac{2}{3}=\frac{1}{4}\). In total \(\frac{1}{3}+\frac{1}{4}=\frac{7}{12}\) is done, so \(\frac{5}{12}\) is left."),
       r'\[\frac{5}{12}\ \tri{són}{son}{is}\ 50\ \text{m}^2\ \to\ 50:\frac{5}{12}=\frac{50\cdot12}{5}=\boxed{120\ \text{m}^2}\]'))
ck(Fr(3, 8) * Fr(2, 3), Fr(1, 4)); ck(1 - Fr(1, 3) - Fr(1, 4), Fr(5, 12)); ck(50 / Fr(5, 12), 120)
