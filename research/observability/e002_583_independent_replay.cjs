#!/usr/bin/env node
// E002-583 independent Node.js source replay. No Python parser or sampler reused.
// Output is aggregate only; original human annotations are never committed.
'use strict';
const fs=require('node:fs'), crypto=require('node:crypto'), cp=require('node:child_process');
const SHA='a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223';
function fail(s){throw Error(s);}
function parse(buf){
  const out=[];
  for(const line of buf.toString('latin1').split(/\r?\n/)){
    const t=line.trim();
    if(!/^\d/.test(t))continue;
    const f=t.split(/[,:;\t ]+/).filter(Boolean);
    if(f.length!==19 || !/^\d+$/.test(f[0]))fail('BAD_SCHEMA');
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
  return n>=0 && (n%10===0||n%10===3||n%10===6);
}
function analyze(rows,kind){
  const totals={candidate_runs:0,eligible_runs:0,boundary_abstain:0,missing_index_abstain:0,
    nuisance_abstain:0,phase_law_checked:0,runs_omitted_any_phase:0,runs_omitted_all_phases:0};
  const hist=[0,0,0,0],phases=Array(10).fill(0);
  const isPos=r=>kind==='both'?(r.l==='C'&&r.r==='C'):(r.l==='C'||r.r==='C');
  const first=rows[0].id,last=rows.at(-1).id;
  for(let i=0;i<rows.length;i++){
    if(!isPos(rows[i]))continue;
    const a=i;
    while(i+1<rows.length&&isPos(rows[i+1])&&rows[i+1].id===rows[i].id+1)i++;
    const b=i;totals.candidate_runs++;
    if(a===0||b===rows.length-1||rows[a].id<first+10||rows[b].id>last-10){
      totals.boundary_abstain++;continue;
    }
    const span=rows.slice(a-1,b+2);
    if(span.some((r,j)=>j>0&&r.id!==span[j-1].id+1)){
      totals.missing_index_abstain++;continue;
    }
    if(span.some(r=>r.nf==='N'||r.ln==='N'||r.rn==='N')){
      totals.nuisance_abstain++;continue;
    }
    totals.eligible_runs++;
    const len=b-a+1;hist[Math.min(len,4)-1]++;
    let misses=0;
    for(let phase=0;phase<10;phase++){
      let detected=false;
      for(let j=a;j<=b;j++)if(sampled(rows[j].id,first,phase)){detected=true;break;}
      if(!detected){misses++;phases[phase]++;}
    }
    if(misses!==(len===1?7:len===2?4:len===3?1:0))fail('PHASE_LAW_FALSIFIED');
    totals.phase_law_checked++;
    if(misses>0)totals.runs_omitted_any_phase++;
    if(misses===10)totals.runs_omitted_all_phases++;
  }
  return {totals,hist,phases};
}
function main(file){
  const zip=fs.readFileSync(file);
  if(crypto.createHash('sha256').update(zip).digest('hex')!==SHA)fail('SHA_CHANGED');
  const names=cp.execFileSync('unzip',['-Z','-1',file],{encoding:'utf8',maxBuffer:2e6})
    .split(/\r?\n/).filter(n=>n.toLowerCase().endsWith('.tag'));
  if(names.length!==5)fail('SEQUENCES_CHANGED');
  const out={experiment:'E002-583',independent_replay:'Node.js',source_rows:0,
    source_sequences:5,both:{},either:{}};
  for(const kind of ['both','either']){
    const totals={candidate_runs:0,eligible_runs:0,boundary_abstain:0,missing_index_abstain:0,
      nuisance_abstain:0,phase_law_checked:0,runs_omitted_any_phase:0,runs_omitted_all_phases:0};
    const hist=[0,0,0,0],phases=Array(10).fill(0);
    let rowsCount=0;
    for(const name of names){
      if(name.includes('..')||name.startsWith('/')||name.includes('\\'))fail('UNSAFE_MEMBER');
      const rows=parse(cp.execFileSync('unzip',['-p',file,name],{maxBuffer:3e7}));
      rowsCount+=rows.length;
      const a=analyze(rows,kind);
      for(const k of Object.keys(totals))totals[k]+=a.totals[k];
      for(let j=0;j<4;j++)hist[j]+=a.hist[j];
      for(let j=0;j<10;j++)phases[j]+=a.phases[j];
    }
    if(rowsCount!==58884)fail('ROW_COUNT_CHANGED');
    out.source_rows=rowsCount;
    out[kind]={counts:totals,length_histogram:{'1':hist[0],'2':hist[1],'3':hist[2],'4+':hist[3]},omitted_by_phase:phases};
  }
  out.physical_shutter_verified=false;
  console.log(JSON.stringify(out));
}
if(process.argv.length!==3)fail('USAGE: node replay.cjs ARCHIVE.zip');
main(process.argv[2]);
