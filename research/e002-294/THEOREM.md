# Exact periodic hidden-dose theorem

Let c(t) in [0,1] be V-Lipschitz and periodic with P=T+G. Exposure [0,T] reports m=(1/T)int_0^T c(t)^p dt, p>=1, observed with additive |e|<=eta. The gap is [T,P]. Null: c=0. Alternative: arbitrary periodic c satisfying the same bounds. An observational collision occurs iff m<=2eta.

Put r=min(1,2eta), M_p(x)=2[x^(p+1)-(x-VT/2)_+^(p+1)]/((p+1)VT), and x*=max{x in [0,1]:M_p(x)<=r}. Then the exact largest gap closure dose among alternatives observationally indistinguishable from the null is

U=int_0^G min(1,x*+V min(s,G-s))ds
 = x*G+VG^2/4 if x*+VG/2<=1,
 = G-(1-x*)^2/V otherwise.

The exact largest hidden gap peak is min(1,x*+VG/2).

For p=1, x*=min(1,sqrt(rVT)) when r<=VT/4, otherwise x*=min(1,r+VT/4). At eta=0, U=VG^2/4 if VG<=2, otherwise G-1/V.

**Proof:** Reflect any periodic admissible waveform about the exposure midpoint, which preserves the exposure and gap intervals. The reflection has the same gap dose and exposure mean. Average the waveform and reflection. The gap dose is unchanged; exposure mean does not increase by convexity of c^p. The symmetrized waveform has identical exposure endpoints x. On the exposure the V-Lipschitz lower envelope is max(0,x-V min(t,T-t)), whose pth-power average is M_p(x). Thus x<=x*. On the gap the upper envelope is min(1,x+V min(t,G-t)); its integral increases in x. Both envelopes join continuously, attain the bound, and define a periodic V-Lipschitz waveform. Set observed y=m/2: under H0 use error +m/2, under H1 use -m/2, both bounded by eta. This establishes a sharp collision.

**Exact witnesses:** T=G=V=1, x=1/4. Exposure waveform max(0,1/4-min(t,1-t)); gap waveform 1/4+min(t-1,2-t). Hidden gap dose=1/2, peak=3/4. Linear response has m=1/16 and eta=1/32; quadratic response has m=1/96 and eta=1/192. Both collide exactly with the open-eye null.

**Limitations:** Sharp only for the periodic model, not arbitrary finite nonperiodic recordings. f must be independently calibrated; an unknown arbitrarily flat response defeats certification. V must be a defensible worst-case bound, not an average. Rolling shutter, ISP, glasses, gaze, lighting and frame drops may violate assumptions. This does not identify fatigue, PERCLOS, individual blinks or physiological mechanism. No human RGB/reference test performed. Mathematical techniques are established optimal-recovery prior art.