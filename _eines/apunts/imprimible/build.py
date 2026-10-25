# Versió imprimible (PDF A4) dels apunts interactius d'una unitat.
# Agafa la pàgina d'apunts, n'amaga tot el que és interactiu (índex, eines, resolutor, autoavaluació, botons,
# solucions desplegables), mostra tots els passos dels exemples i hi posa la capçalera 6 («Apunts web»):
# banda blava amb el logo, el curs i la unitat, l'etiqueta «Apunts» i el títol (sense descripció ni xips).
# Després la imprimeix amb Chrome (protocol DevTools, només amb la biblioteca estàndard de Python) amb el peu de pàgina
# de les fitxes d'exercicis: icones CC BY-NC-SA (ccbyncsa.png, fetes amb ccicons de LaTeX), llicència i número de pàgina.
# Ús: python3 _eines/apunts/imprimible/build.py materials/2batx-ccss/t3-programacio-lineal.html [eixida.pdf]
import os, re, sys, subprocess, json, base64, socket, time, tempfile, shutil, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CURS = {'2batx-ccss': ('2n Batxillerat CCSS', '#2bb3a3'), '2batx-mii': ('2n Batxillerat CT', '#1e6b47'),
        '1eso': ('1r ESO', '#e6b84a'), '3eso': ('3r ESO', '#ff7a50')}

src = os.path.join(ROOT, sys.argv[1])
course = re.search(r'materials/([^/]+)/', sys.argv[1]).group(1)
out = sys.argv[2] if len(sys.argv) > 2 else src.replace('.html', '-imprimible.pdf')
page = open(src, encoding='utf-8').read()

# títol i número d'unitat a partir del banner (versió en valencià)
h1 = re.search(r'<h1>(.*?)</h1>', page, re.S).group(1)
va = re.findall(r'<span data-l="va">(.*?)</span>', h1)
unitat, titol = va[0], va[-1]
curs, color = CURS[course]

CAP = f'''<header class="ph">
  <div class="ph-nav"><img src="../../assets/img/logo/horitzontal-fosc.svg" alt="FentMates"><span>{curs} · {unitat}</span></div>
  <span class="ph-k">Apunts</span>
  <h1>{titol}</h1>
  <img class="ph-deco" src="../../assets/img/logo/marca-blanc.svg" alt="">
</header>'''

CSS = f'''<style>
/* ---- versió imprimible ---- */
* {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
html, body {{ background: #fff !important; }}
body {{ font-size: 10pt; line-height: 1.5; }}
.box > .bb {{ padding: 4px 16px 10px; }}
.topbar, .hero, .toc, .steps-ctl, .done-btn, .to-top, .widget, .quiz-sec, #lab, footer.foot, details.sol {{ display: none !important; }}
.layout {{ display: block !important; padding: 0 !important; max-width: none !important; }}
article {{ max-width: none !important; }}
.steps.js > .step.hidden {{ display: block !important; }}
section.unit {{ margin-bottom: 14px; }}
.sec-head {{ break-after: avoid; margin-bottom: 10px; }}
.sec-head .num {{ width: 40px; height: 40px; }}
/* els quadres no es parteixen entre pàgines, llevat dels molt llargs (classe llarg, posada abans d'imprimir) */
.box {{ break-inside: avoid; margin: 12px 0; }}
.box.llarg {{ break-inside: auto; }}  /* quadres més llargs que mitja pàgina: es parteixen entre exemples o passos */
.box > .bh {{ break-after: avoid; }}
.box .katex-display, figure.plfig, .tbl-wrap, .note, .step, .ex-list > li {{ break-inside: avoid; }}
figure.plfig {{ max-width: 240px; margin: 6px auto; }}
.legend {{ font-size: 8.5pt; }}
.two figure.plfig {{ max-width: 220px; }}
h3.sub {{ break-after: avoid; }}
/* capçalera 6 */
.ph {{ position: relative; overflow: hidden; margin: 0 0 9mm; padding: 4.5mm 7mm 5mm; border-radius: 3mm; color: #fff;
  background: linear-gradient(120deg, #1b2748 0%, #24375f 70%, #2c4475 100%); }}
.ph-nav {{ display: flex; justify-content: space-between; align-items: center; font: 500 9pt Inter, sans-serif; color: #c3cbe2; position: relative; z-index: 1; }}
.ph-nav img {{ height: 8.5mm; }}
.ph-k {{ display: inline-block; margin-top: 3.5mm; padding: .4mm 3mm; border-radius: 99px; font: 600 8pt Inter, sans-serif;
  background: color-mix(in srgb, {color} 24%, transparent); color: color-mix(in srgb, {color} 50%, #fff); position: relative; z-index: 1; }}
.ph h1 {{ margin: 1.5mm 0 0; font: 800 24pt/1.05 Outfit, sans-serif; color: #fff; position: relative; z-index: 1; }}
.ph-deco {{ position: absolute; right: 6mm; bottom: -9mm; height: 40mm; opacity: .08; }}
</style>'''

page = page.replace('</head>', CSS + '\n</head>', 1)
page = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + CAP, page, count=1)
tmp = src.replace('.html', '-tmpprint.html')  # el nom ha de començar per tN perquè fm-materials.js trobe el bloc
open(tmp, 'w', encoding='utf-8').write(page)

# peu de pàgina (com a les fitxes): icones CC, llicència i número de pàgina
CC = base64.b64encode(open(os.path.join(HERE, 'ccbyncsa.png'), 'rb').read()).decode()
PEU = ('<div style="width:100%;margin:0 13mm;display:flex;align-items:center;gap:2.5mm;font:7pt Helvetica,Arial,sans-serif;color:#5d6685">'
       '<img src="data:image/png;base64,' + CC + '" style="height:3.3mm">'
       '<span>Llicència Creative Commons Reconeixement-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)</span>'
       '<span style="margin-left:auto;font-size:8.5pt" class="pageNumber"></span></div>')

# espera que acaben KaTeX, les fonts i les gràfiques
WAIT = ('new Promise(r => { const ok = () => document.readyState === "complete" && document.querySelectorAll(".katex").length > 0;'
        ' const t = () => ok() ? document.fonts.ready.then(() => setTimeout(r, 800)) : setTimeout(t, 200); t(); })')

# ---------- client mínim del protocol DevTools (websocket) ----------
class WS:
    def __init__(self, url):
        host, port, path = re.match(r'ws://([^:/]+):(\d+)(/.*)', url).groups()
        self.s = socket.create_connection((host, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(('GET %s HTTP/1.1\r\nHost: %s:%s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        'Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n' % (path, host, port, key)).encode())
        buf = b''
        while b'\r\n\r\n' not in buf: buf += self.s.recv(4096)
        self.rest = buf.split(b'\r\n\r\n', 1)[1]
        self.n = 0
    def _read(self, k):
        while len(self.rest) < k:
            d = self.s.recv(1 << 20)
            if not d: raise EOFError
            self.rest += d
        r, self.rest = self.rest[:k], self.rest[k:]
        return r
    def recv(self):
        msg = b''
        while True:
            b1, b2 = self._read(2)
            ln = b2 & 127
            if ln == 126: ln = int.from_bytes(self._read(2), 'big')
            elif ln == 127: ln = int.from_bytes(self._read(8), 'big')
            msg += self._read(ln)
            if b1 & 0x80: return json.loads(msg)
    def call(self, method, **params):
        self.n += 1
        data = json.dumps({'id': self.n, 'method': method, 'params': params}).encode()
        n = len(data)
        hdr = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + n.to_bytes(2, 'big') if n < 65536
                               else bytes([0x80 | 127]) + n.to_bytes(8, 'big'))
        mask = os.urandom(4)
        self.s.sendall(hdr + mask + bytes(c ^ mask[i % 4] for i, c in enumerate(data)))
        while True:
            m = self.recv()
            if m.get('id') == self.n:
                if 'error' in m: raise RuntimeError(m['error'])
                return m['result']

prof = tempfile.mkdtemp()
port = 9300 + os.getpid() % 500
chrome = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--remote-debugging-port=%d' % port, '--user-data-dir=' + prof,
                           '--no-first-run', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    tabs = None
    for _ in range(150):
        try:
            tabs = json.load(urllib.request.urlopen('http://127.0.0.1:%d/json/list' % port)); break
        except Exception: time.sleep(0.1)
    ws = WS([t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl'])
    ws.call('Page.navigate', url='file://' + tmp + '?lang=va')
    time.sleep(0.5)
    ws.call('Runtime.evaluate', expression=WAIT, awaitPromise=True)
    # maquetació amb l'ample útil de l'A4 (7,25 polzades = 696 px) i mitjans d'impressió, per mesurar els quadres
    ws.call('Emulation.setDeviceMetricsOverride', width=696, height=1015, deviceScaleFactor=1, mobile=False)
    ws.call('Emulation.setEmulatedMedia', media='print')
    ws.call('Runtime.evaluate', awaitPromise=True, expression='new Promise(r => setTimeout(() => { document.querySelectorAll(".box").forEach(b => '
            '{ if (b.getBoundingClientRect().height > 560) b.classList.add("llarg"); }); r(); }, 600))')
    pdf = ws.call('Page.printToPDF', printBackground=True, displayHeaderFooter=True, headerTemplate='<span></span>', footerTemplate=PEU,
                  paperWidth=8.27, paperHeight=11.69, marginTop=0.5, marginBottom=0.62, marginLeft=0.51, marginRight=0.51,
                  preferCSSPageSize=False)
    open(out, 'wb').write(base64.b64decode(pdf['data']))
finally:
    chrome.terminate(); chrome.wait()
    shutil.rmtree(prof, ignore_errors=True)
    os.remove(tmp)
print('PDF:', os.path.relpath(out, ROOT))
