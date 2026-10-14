"""Strict EyeBlink8 parser. ID zero denotes a valid blink."""
def parse(text):
    lines=text.splitlines()
    a=[i for i,s in enumerate(lines) if s.strip()=="#start"]
    b=[i for i,s in enumerate(lines) if s.strip()=="#end"]
    if len(a)!=1 or len(b)!=1 or b[0]<=a[0]:
        raise ValueError("invalid annotation delimiters")
    out=[]
    for line in lines[a[0]+1:b[0]]:
        if not line.strip() or line.lstrip().startswith("#"): continue
        fields=line.split(":")
        if len(fields)!=19: raise ValueError("invalid field count")
        frame,blink=map(int,fields[:2])
        if blink < -1 or (out and frame<=out[-1][0]):
            raise ValueError("invalid frame or blink ID")
        out.append((frame,blink))
    if not out: raise ValueError("empty annotation")
    return out
