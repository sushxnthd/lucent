#!/usr/bin/env node
// E002-582 independent Node.js replay of original human FC annotations.
// No reuse of the Python parser or phase enumeration. No images or raw rows logged.
// Input: local source ZIP from official public annotation URL, never commit it.
'use strict';
const fs = require('node:fs');
const crypto = require('node:crypto');
const cp = require('node:child_process');

const SOURCE_SHA = 'a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223';
const EXPECTED = {rows:58884, runs:567, lengths:[7,28,41,491],
  phases:[29,18,21,17,20,18,25,20,14,20], any:76};

function fail(code) { throw new Error(code); }
function parseTag(raw) {
  const rows = [];
  for (const line of raw.toString('latin1').split(/\r?\n/)) {
    const text = line.trim();
    if (!/^\d/.test(text)) continue;
    const f = text.split(/[,:;\t ]+/).filter(Boolean);
    if (f.length !== 19 || !/^\d+$/.test(f[0])) fail('INVALID_TAG_ROW');
    if (!['X','N'].includes(f[2]) || !['X','N'].includes(f[4]) ||
        !['X','N'].includes(f[6]) || !['X','C'].includes(f[3]) ||
        !['X','C'].includes(f[5])) fail('INVALID_SOURCE_FLAGS');
    const id = Number(f[0]);
    if (!Number.isSafeInteger(id) || (rows.length && id <= rows.at(-1).id)) fail('BAD_FRAME_INDEX');
    rows.push({id, nf:f[2], fc:[f[3],f[5]], nv:[f[4],f[6]]});
  }
  return rows;
}

function isSampled(index, origin, phase) {
  const relative = index - origin - phase;
  return relative >= 0 && [0,3,6].includes(relative % 10);
}

function analyzeOne(rows) {
  const count = {runs:0, eligible:0, any:0, length:[0,0,0,0],
                 phases:Array(10).fill(0), interior:0};
  const origin = rows[0].id;
  for (let eye=0; eye<2; eye++) {
    for (let i=0; i<rows.length; i++) {
      if (rows[i].fc[eye] !== 'C') continue;
      const start=i;
      while (i+1<rows.length && rows[i+1].fc[eye]==='C' &&
             rows[i+1].id===rows[i].id+1) i++;
      const end=i;
      count.runs++;
      if (start===0 || end===rows.length-1) continue;
      const span=rows.slice(start-1,end+2);
      if (span.some((r,j)=>r.nf==='N' || r.nv[eye]==='N' ||
           (j>0 && r.id!==span[j-1].id+1))) continue;
      count.eligible++;
      const L=end-start+1;
      count.length[Math.min(L,4)-1]++;
      let omitted=0;
      for (let phase=0;phase<10;phase++) {
        let seen=false;
        for (let t=start;t<=end;t++) {
          if (isSampled(rows[t].id,origin,phase)) {seen=true;break;}
        }
        if (!seen) {count.phases[phase]++; omitted++;}
      }
      if (omitted) count.any++;
      if (rows[start].id >= origin+10 && rows[end].id <= rows.at(-1).id-10) {
        count.interior++;
        const exact=L===1?7:L===2?4:L===3?1:0;
        if (omitted!==exact) fail('INDEPENDENT_PHASE_LAW_MISMATCH');
      }
    }
  }
  return count;
}

function main(path) {
  const zip=fs.readFileSync(path);
  if (crypto.createHash('sha256').update(zip).digest('hex')!==SOURCE_SHA) fail('SOURCE_SHA_MISMATCH');
  const names=cp.execFileSync('unzip',['-Z','-1',path],{encoding:'utf8',maxBuffer:2e6})
    .split(/\r?\n/).filter(n=>n.toLowerCase().endsWith('.tag'));
  if (names.length!==5) fail('EXPECTED_FIVE_TAG_FILES');
  let frames=0, runs=0, eligible=0, any=0, interior=0;
  const lengths=[0,0,0,0], phases=Array(10).fill(0);
  for (const name of names) {
    if (name.includes('..') || name.startsWith('/') || name.includes('\\')) fail('UNSAFE_ZIP_MEMBER');
    const raw=cp.execFileSync('unzip',['-p',path,name],{maxBuffer:3e7});
    const rows=parseTag(raw);
    frames+=rows.length;
    const a=analyzeOne(rows);
    runs+=a.runs;eligible+=a.eligible;any+=a.any;interior+=a.interior;
    for(let i=0;i<4;i++)lengths[i]+=a.length[i];
    for(let i=0;i<10;i++)phases[i]+=a.phases[i];
  }
  if(frames!==EXPECTED.rows || runs!==EXPECTED.runs || eligible!==EXPECTED.runs ||
     any!==EXPECTED.any || interior!==EXPECTED.runs ||
     JSON.stringify(lengths)!==JSON.stringify(EXPECTED.lengths) ||
     JSON.stringify(phases)!==JSON.stringify(EXPECTED.phases)) fail('INDEPENDENT_REPLAY_DIVERGENCE');
  console.log(JSON.stringify({experiment:'E002-582',independent_replay:'PASS',
    implementation:'Node.js integer-residue replay, not Python code',
    frames,runs,eligible,any,interior,lengths,phases,
    evidence_tier:'HUMAN_FC_LABEL_INDEX_ONLY',physical_shutter_validated:false}));
}

if(process.argv.length!==3) fail('USAGE_NODE_SCRIPT_ARCHIVE_PATH');
main(process.argv[2]);
