import math,sys
phi=(1+5**.5)/2
def spiral(x0,y0,H,n,stroke_sq,stroke_arc,arc_w,sq_op):
    # rectangle width H*phi, height H, squares placed left,top,right,bottom...
    x,y,w,h=x0,y0,H*phi,H
    sq=[];arcs=[]
    d=0
    for i in range(n):
        s=min(w,h)
        if d==0:   # square at left
            sx,sy=x,y; x+=s; w-=s
            cx,cy=sx+s,sy+s; a0,a1=180,270
        elif d==1: # top
            sx,sy=x,y; y+=s; h-=s
            cx,cy=sx,sy+s; a0,a1=270,360
        elif d==2: # right
            sx,sy=x+w-s,y; w-=s
            cx,cy=sx,sy; a0,a1=0,90
        else:      # bottom
            sx,sy=x,y+h-s; h-=s
            cx,cy=sx+s,sy; a0,a1=90,180
        sq.append((sx,sy,s))
        p0=(cx+s*math.cos(math.radians(a0)),cy+s*math.sin(math.radians(a0)))
        p1=(cx+s*math.cos(math.radians(a1)),cy+s*math.sin(math.radians(a1)))
        arcs.append((p0,p1,s))
        d=(d+1)%4
    out=[]
    for sx,sy,s in sq:
        out.append(f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{s:.1f}" height="{s:.1f}" fill="none" stroke="{stroke_sq}" stroke-opacity="{sq_op}" stroke-width="2"/>')
    path="M%.1f %.1f"%arcs[0][0]
    for p0,p1,s in arcs:
        path+=" A%.1f %.1f 0 0 1 %.1f %.1f"%(s,s,p1[0],p1[1])
    out.append(f'<path d="{path}" fill="none" stroke="{stroke_arc}" stroke-width="{arc_w}" stroke-linecap="round"/>')
    return "\n".join(out),sq
body,sq=spiral(1150,0,600,12,"#9ec5ff","#6fb6ff",5,".22")
ga=math.pi*(3-5**.5)
dots=[]
for i in range(1,230):
    r=7.2*i**.5; th=i*ga
    x=210+r*math.cos(th); y=330+r*math.sin(th)
    rad=1.6+i/230*3.2
    dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="#9ec5ff" fill-opacity="{.10+i/230*.22:.2f}"/>')
cx,cy,R=420,180,58
pts=[(cx+R*math.cos(math.radians(-90+72*k)),cy+R*math.sin(math.radians(-90+72*k))) for k in range(5)]
pent=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
star=" ".join(f"{pts[k][0]:.1f},{pts[k][1]:.1f}" for k in (0,2,4,1,3))
small="\n".join(dots)+f'<polygon points="{pent}" fill="none" stroke="#9ec5ff" stroke-opacity=".28" stroke-width="2"/><polygon points="{star}" fill="none" stroke="#6fb6ff" stroke-opacity=".45" stroke-width="2"/>'
# numbers inside the biggest squares
fib=[89,55,34,21,13,8,5,3]
labels="".join(f'<text x="{2*1150+600*phi-(sx+s/2):.0f}" y="{sy+s/2+s*0.09:.0f}" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="{s*0.26:.0f}" fill="#cfe2ff" fill-opacity=".09">{f}</text>' for (sx,sy,s),f in list(zip(sq[:6],fib))[1:])
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 600" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f1f3d"/>
      <stop offset="0.55" stop-color="#16315f"/>
      <stop offset="1" stop-color="#1e4b8a"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.72" cy="0.55" r="0.55">
      <stop offset="0" stop-color="#5aa9ff" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#5aa9ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="veil" cx="800" cy="290" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(800 290) scale(430 190) translate(-800 -290)">
      <stop offset="0" stop-color="#000"/>
      <stop offset="0.72" stop-color="#000"/>
      <stop offset="1" stop-color="#fff"/>
    </radialGradient>
    <mask id="clear" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="600">
      <rect width="1600" height="600" fill="url(#veil)"/>
    </mask>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.045" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="1600" height="600" fill="url(#bg)"/>
  <rect width="1600" height="600" fill="url(#grid)"/>
  <rect width="1600" height="600" fill="url(#glow)"/>
  <g transform="translate({2*1150+600*phi:.1f} 0) scale(-1 1)">
  {body}
  </g>
  {labels}
  <g>{small}</g>
  <g font-family="Georgia,serif" font-style="italic" fill="#cfe2ff">
    <text x="70" y="80" font-size="34" fill-opacity=".16">φ = (1 + √5) / 2</text>
    <text x="1545" y="585" text-anchor="end" font-size="26" fill-opacity=".15">1, 1, 2, 3, 5, 8, 13, 21…</text>
  </g>
</svg>'''
open(sys.argv[1],"w").write(svg)
