// E002-256: deterministic participant-cluster bootstrap of pinned human aggregate decomposition.
// Descriptive variability only: checkpoint train/test overlap unknown, NOT prospective inference.
import {createHash} from 'node:crypto';
import {writeFileSync} from 'node:fs';
const COMMIT='aa9bddf498a3b6e4104c2c000d2cc0c06a816aae';
const PINS={left:['per_participant_left_eye.csv','509e14d61455dc6ee119a0fc2ba9e7448eedc9fc'],right:['per_participant_right_eye.csv','9f55dd52fc6c11c9903ec9c7b0c735192cd4a790']};
let seed=2562026;
const random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296;};
function decomp(rows){
 const N=rows.reduce((v,x)=>v+x.n,0),mx=rows.reduce((v,x)=>v+x.n*x.xm,0)/N,my=rows.reduce((v,x)=>v+x.n*x.ym,0)/N;
 let wxy=0,wxx=0,wyy=0,bxy=0,bxx=0,byy=0;
 for(const x of rows){wxy+=(x.n-1)*x.r*x.sx*x.sy;wxx+=(x.n-1)*x.sx*x.sx;wyy+=(x.n-1)*x.sy*x.sy;bxy+=x.n*(x.xm-mx)*(x.ym-my);bxx+=x.n*(x.xm-mx)**2;byy+=x.n*(x.ym-my)**2;}
 return {fraction:bxy/(wxy+bxy),centered_r:wxy/Math.sqrt(wxx*wyy),pooled_r:(wxy+bxy)/Math.sqrt((wxx+bxx)*(wyy+byy))};
}
const quantile=(xs,p)=>{xs.sort((a,b)=>a-b);const j=(xs.length-1)*p,k=Math.floor(j);return xs[k]+(xs[Math.min(k+1,xs.length-1)]-xs[k])*(j-k);};
const out={seed:2562026,replicates:5000,bootstrap_unit:'participant',method:'percentile cluster bootstrap; descriptive not prospective'};
for(const eye of ['left','right']){
 const [filename,pin]=PINS[eye];
 const url='https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/'+COMMIT+'/output/'+filename;
 const response=await fetch(url);if(!response.ok)throw new Error('source unavailable '+eye);
 const bytes=Buffer.from(await response.arrayBuffer());
 const sha=createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
 if(sha!==pin)throw new Error('SOURCE_IDENTITY_FAIL '+eye);
 const rows=bytes.toString('utf8').trim().split(/\r?\n/).slice(1).map(line=>{const q=line.split(',').map(Number);return {n:q[1],ym:q[4],xm:q[4]+q[3],sy:q[5],sx:q[6],r:q[7]};});
 if(rows.length!==51)throw new Error('participant count');
 const fractions=[],cent=[];
 for(let j=0;j<5000;j++){
   const sample=Array.from({length:rows.length},()=>rows[Math.floor(random()*rows.length)]);
   const x=decomp(sample);fractions.push(x.fraction);cent.push(x.centered_r);
 }
 const frac_above_half=fractions.filter(x=>x>.5).length/fractions.length;
 out[eye]={point:decomp(rows),between_cov_fraction_95pct:[quantile(fractions,.025),quantile(fractions,.975)],centered_r_95pct:[quantile(cent,.025),quantile(cent,.975)],fraction_above_half:frac_above_half};
}
writeFileSync('research/e002-256/CI_BOOTSTRAP.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out));
