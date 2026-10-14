"""Five-second annotation observables; never equate count with fatigue."""
def windows(rows,width=150,shift=0):
    by_frame=dict(rows)
    censored=set()
    onsets=set()
    for i,(frame,blink) in enumerate(rows):
        if blink<0: continue
        if i==0 or rows[i-1][0]!=frame-1:
            censored.add(frame)
        elif rows[i-1][1]!=blink:
            onsets.add(frame)
    out=[]
    for a in range(rows[0][0]+shift,rows[-1][0]-width+2,width):
        b=a+width
        if all(t in by_frame for t in range(a,b)) and not any(a<=t<b for t in censored):
            out.append((a,b,sum(a<=t<b for t in onsets)))
    return out
def expected_zero(counts):
    w=len(counts)
    if not w: return 0.0
    return w*((w-1)/w)**sum(counts)
