#!/usr/bin/env python3
"""Source-faithful synthetic audit of EyeDentify rowwise mean; no human data."""
import csv,json,math,pathlib
P=pathlib.Path(__file__).resolve().parent
N=90
def fold(x):
    assert len(x)==270
    return [(x[j]+x[90+j]+x[180+j])/3 for j in range(N)]
def sine(f,rate,n):return [math.sin(2*math.pi*f*j/rate) for j in range(n)]
def rms(x):return math.sqrt(sum(v*v for v in x)/len(x))
def corr(a,b):
    u=[v-sum(a)/len(a) for v in a];w=[v-sum(b)/len(b) for v in b]
    d=math.sqrt(sum(v*v for v in u)*sum(v*v for v in w))
    return sum(v*t for v,t in zip(u,w))/d if d>1e-10 else None
def main():
    x=[math.sin(.17*j)+.003*j for j in range(270)];z=x[:]
    for j in range(N):
        z[j]+=math.cos(.13*j);z[N+j]-=math.cos(.13*j)
    freqs=[]
    for f in (1/3,.5,1.,2.):
        y=fold(sine(f,90,270));cam=sine(f,30,90)
        h=sum(complex(math.cos(2*math.pi*f*k),math.sin(2*math.pi*f*k)) for k in range(3))/3
        freqs.append(dict(f_hz=f,label_rms=rms(y),perfect_webcam_r=corr(y,cam),perfect_webcam_rmse=rms([a-b for a,b in zip(y,cam)]),fold_gain=abs(h)))
    label=fold([j/90 for j in range(270)]);truth=[j/30 for j in range(N)]
    err=[a-b for a,b in zip(label,truth)]
    out=dict(run="E002-216",synthetic_only=True,source_git_blob_sha1="f46d7ae369a62596f7044ca647d361c38fcb16ea",assumptions=dict(tracker_hz=90,webcam_fps=30,seconds=3,samples_per_block=90),fold_map_shape=[90,270],exact_rank=90,exact_nullity=180,collision_max_abs_error=max(abs(a-b) for a,b in zip(fold(x),fold(z))),ramp_start_error_seconds=err[0],ramp_end_error_seconds=err[-1],ramp_rmse_seconds=rms(err),frequencies=freqs)
    (P/"RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
    with (P/"RAW_SYNTHETIC.csv").open("w",newline="") as h:
        w=csv.writer(h);w.writerow(["frame","webcam_t_s","tracker_fold_label_ramp_s","true_ramp_s","error_s","perfect_webcam_sine_1hz","folded_sine_1hz"])
        a=fold(sine(1,90,270));b=sine(1,30,N)
        for j in range(N):w.writerow([j,j/30,label[j],truth[j],err[j],b[j],a[j]])
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
