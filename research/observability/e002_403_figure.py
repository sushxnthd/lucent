#!/usr/bin/env python3
"""Generate an SVG of the frozen E002-403 shutter-kernel counterexample."""
from pathlib import Path

OUT=Path(__file__).with_name('E002_403_SHUTTER_KERNEL.svg')
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="650" viewBox="0 0 1000 650">
<rect width="1000" height="650" fill="#ffffff"/>
<g font-family="Arial,Helvetica,sans-serif" fill="#15283a">
<text x="74" y="49" font-size="23" font-weight="700">Shutter response changes the observability verdict</text>
<text x="74" y="73" font-size="13" fill="#4e6473">E002-403 | exact synthetic counterexample | normalized aperture, time in milliseconds</text>
</g>
''']
def line(x1,y1,x2,y2,color='#c8d4dc',width=1,dash=''):
    parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def text(x,y,s,size=13,color='#15283a',weight='400'):
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{s}</text>')
def poly(points,color,width=3):
    parts.append('<polyline fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" points="%s"/>'%(color,width,' '.join(f'{x:.2f},{y:.2f}' for x,y in points)))
x0,x1=95,915
def x(t):return x0+(t+5)/20*(x1-x0)
def y1(a):return 337-(a-.10)/.35*190
def y2(a):return 585-(a-.15)/.23*160
# Upper panel
text(95,109,'A  |  True aperture and exposure windows',15,weight='700')
for val in (.1,.2,.3,.4):
    yy=y1(val);line(95,yy,915,yy,'#e4ebef',1)
    text(53,yy+4,f'{val:.1f}',12,'#607382')
parts.append(f'<rect x="{x(-5):.2f}" y="137" width="{x(5)-x(-5):.2f}" height="195" fill="#e6f2f8" opacity=".48"/>')
parts.append(f'<rect x="{x(5):.2f}" y="137" width="{x(15)-x(5):.2f}" height="195" fill="#f2eaf5" opacity=".45"/>')
for t in (-5,15):
    line(x(t),137,x(t),332,'#758e9b',1,'5,4')
# Temporal response pulses (0.2 ms)
parts.append(f'<rect x="{x(-5):.2f}" y="137" width="{x(-4.8)-x(-5):.2f}" height="195" fill="#c16a36" opacity=".28"/>')
parts.append(f'<rect x="{x(14.8):.2f}" y="137" width="{x(15)-x(14.8):.2f}" height="195" fill="#c16a36" opacity=".28"/>')
poly([(x(-5+i*20/400),y1(.19+20*abs((-5+i*20/400)/1000-.005))) for i in range(401)],'#235c83',3)
line(95,y1(.2),915,y1(.2),'#c24a52',2,'6,5')
text(700,y1(.2)-8,'Closure threshold = 0.20',12,'#a5343c')
parts.append(f'<circle cx="{x(5):.2f}" cy="{y1(.19):.2f}" r="5" fill="#c24a52"/>')
text(x(5)+12,y1(.19)+22,'True minimum = 0.19',12,'#a5343c')
for t in (0,10):
    line(x(t),138,x(t),337,'#667e8d',1,'4,4')
    text(x(t)-18,354,f'{t} ms',12,'#415b6a')
text(105,129,'Outer-edge pulses produce measured mean = 0.388 in both frames',12,'#98562d')
# Lower panel
text(95,404,'B  |  Lower envelopes under different shutter assumptions',15,weight='700')
for val in (.2,.3):
    yy=y2(val);line(95,yy,915,yy,'#e4ebef')
    text(53,yy+4,f'{val:.1f}',12,'#607382')
line(95,y2(.2),915,y2(.2),'#c24a52',2,'6,5')
poly([(x(i*10/200),y2(.338-20*min(i*10/200,10-i*10/200)/1000)) for i in range(201)],'#c16a36',3)
poly([(x(i*10/200),y2(.290-20*min(i*10/200,10-i*10/200)/1000)) for i in range(201)],'#247b76',3)
text(550,454,'Incorrect uniform e/4 bound: min 0.238',13,'#a15b2e','700')
text(550,555,'Calibrated temporal moment: min 0.190',13,'#1d6964','700')
text(95,612,'A wrong no-crossing certificate becomes UNRESOLVED when temporal shutter weighting is bounded.',13,'#3b5464')
text(95,632,'Synthetic instrument only. Not a measured camera or human blink result.',11,'#71818b')
parts.append('</svg>')
OUT.write_text('\n'.join(parts)+'\n')
print(OUT)
