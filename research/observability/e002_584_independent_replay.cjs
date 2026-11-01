#!/usr/bin/env node
// E002-584 independent original-source ZIP/TAG replay using modular residues.
// Does not import Python or reuse Python's retained-index enumeration.
'use strict';
const fs=require('node:fs'),crypto=require('node:crypto'),cp=require('node:child_process');
const SHA='a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223';
const expected={both:{eligible:279,nominal:105,j1:4,j2:0},either:{eligible:288,nominal:97,j1:3,j2:0}};
function fail(s){throw Error(s);}
function parse(buf){
  const out=[];
  for(const line of buf.toString('latin1').split(/\r?\n/)){
    const t=line.trim();if(!/^\d/.test(t))continue;
    const f=t.split(/[,:;\t ]+/).filter(Boolean);
    if(f.length!==19||!/^\d+$/.test(f[0]))fail('BAD_SCHEMA');
    if(!['X','N'].includes(f[2])||!['X','N'].includes(f[4])||!['X','N'].includes(f[6])||
       !['X','C'].includes(f[3])||!['X','C'].includes(f[5]))fail('BAD_FLAGS');
    const id=Number(f[0]);
    if(!Number.isSafeInteger(id)||(out.length&&id<=out.at(-1).id))fail('BAD_ID');
    out.push({id,nf:f[2],l:f[3],ln:f[4],r:f[5],rn:f[6]});
  }
  return out;
}
function sampled(id,origin,phase){
  const n=id-origin-phase;
  return n>=0&&(n%10===0||n%10===3||n%10===6);
}
function robustMiss(a,b,origin,phase,j){
  for(let i=a-j;i<=b+j;i++)if(sampled(i,origin,phase))return false;
  return true;
}
function possibleMiss(a,b,origin,phase,j){
  for(let i=a+j;i<=b-j;i++)if(sampled(i,origin,phase))return false;
  return true;
}
function analyze(rows,kind){
  const isPos=r=>kind==='both'?(r.l==='C'&&r.r==='C'):(r.l==='C'||r.r==='C');
  const first=rows[0].id,last=rows.at(-1).id;
  const out={eligible:0,abstain:0,robust:[0,0,0],possible:[0,0,0]};
  for(let i=0;i<rows.length;i++){
    if(!isPos(rows[i]))continue;
    const a=i;
    while(i+1<rows.length&&isPos(rows[i+1])&&rows[i+1].id===rows[i].id+1)i++;
    const b=i;
    if(a===0||b===rows.length-1||rows[a].id<first+10||rows[b].id>last-10){
      out.abstain++;continue;
    }
    const span=rows.slice(a-1,b+2);
    if(span.some((r,k)=>k>0&&r.id!==span[k-1].id+1)||
       span.some(r=>r.nf==='N'||r.ln==='N'||r.rn==='N')){
      out.abstain++;continue;
    }
    out.eligible++;
    for(let phase=0;phase<10;phase++)for(let j=0;j<=2;j++){
      const rm=robustMiss(rows[a].id,rows[b].id,first,phase,j);
      const pm=possibleMiss(rows[a].id,rows[b].id,first,phase,j);
      if(rm&&!pm)fail('CERTIFICATE_ORDER');
      out.robust[j]+=Number(rm);
      out.possible[j]+=Number(pm);
    }
  }
  return out;
}
function main(file){
  if(!robustMiss(5,5,0,0,1)||robustMiss(4,4,0,0,1))fail('SYNTHETIC_GAP_FIXTURE');
  if(robustMiss(5,5,0,0,2)||!possibleMiss(5,5,0,0,1))fail('SYNTHETIC_JITTER_FIXTURE');
  const zip=fs.readFileSync(file);
  if(crypto.createHash('sha256').update(zip).digest('hex')!==SHA)fail('SHA_CHANGED');
  const names=cp.execFileSync('unzip',['-Z','-1',file],{encoding:'utf8',maxBuffer:2e6})
    .split(/\r?\n/).filter(n=>n.toLowerCase().endsWith('.tag'));
  if(names.length!==5)fail('SEQUENCE_COUNT_CHANGED');
  const sequences=names.map(name=>{
    if(name.includes('..')||name.startsWith('/')||name.includes('\\'))fail('UNSAFE_MEMBER');
    return parse(cp.execFileSync('unzip',['-p',file,name],{maxBuffer:3e7}));
  });
  if(sequences.reduce((a,s)=>a+s.length,0)!==58884)fail('ROW_COUNT_CHANGED');
  const out={experiment:'E002-584',independent_replay:'Node.js modular-index source parser',source_rows:58884};
  for(const kind of ['both','either']){
    const acc={eligible:0,abstain:0,robust:[0,0,0],possible:[0,0,0]};
    for(const rows of sequences){
      const r=analyze(rows,kind);
      acc.eligible+=r.eligible;acc.abstain+=r.abstain;
      for(let j=0;j<=2;j++){acc.robust[j]+=r.robust[j];acc.possible[j]+=r.possible[j];}
    }
    if(acc.eligible!==expected[kind].eligible||acc.robust[0]!==expected[kind].nominal||
       acc.robust[1]!==expected[kind].j1||acc.robust[2]!==expected[kind].j2)fail('FROZEN_PREDICTION_FALSIFIED');
    out[kind]=acc;
  }
  out.physical_shutter_verified=false;
  console.log(JSON.stringify(out));
}
if(process.argv.length!==3)fail('USAGE: node e002_584_independent_replay.cjs ARCHIVE.zip');
main(process.argv[2]);
