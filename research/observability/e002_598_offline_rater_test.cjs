#!/usr/bin/env node
"use strict";
/* E002-598: synthetic VM test of the actual offline HTML, no human data. */
const fs=require("node:fs");
const vm=require("node:vm");
const assert=require("node:assert/strict");
const path=require("node:path");
const html=fs.readFileSync(path.join(__dirname,"e002_598_offline_rater.html"),"utf8");
const match=html.match(/<script>([\s\S]*?)<\/script>/);
assert(match,"Missing inline script");
new vm.Script(match[1],{filename:"e002_598_offline_rater.html"});
for(const pattern of [/<script[^>]+src=/i,/https?:\/\//i,/\bfetch\s*\(/,/\bXMLHttpRequest\b/,/\bsendBeacon\b/,/\blocalStorage\b/,/\bsessionStorage\b/,/\bindexedDB\b/,/\bWebSocket\b/,/\bserviceWorker\b/]){
 assert(!pattern.test(html),"Forbidden network/persistence primitive: "+pattern);
}
const elements=new Map(),downloads=[];
const drawing={clearRect(){},drawImage(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},arc(){},fill(){}};
function el(id){
 if(!elements.has(id)){
  const x={files:[],value:"",textContent:"",className:"",onclick:null,
   addEventListener(event,fn){this["_event_"+event]=fn;},
   getBoundingClientRect(){return {left:0,top:0,width:640,height:480};},
   getContext(){return drawing;}};
  elements.set(id,x);
 }
 return elements.get(id);
}
const doc={getElementById:el,body:{appendChild(){}},
 createElement(tag){assert.equal(tag,"a");return {href:"",download:"",click(){downloads.push(this.download);},remove(){}};}};
let lastBlob=null,serial=0;
const fakeURL={createObjectURL(value){if(value instanceof FakeBlob)lastBlob=value;return "blob:test-"+(++serial);},revokeObjectURL(){}};
class FakeBlob{constructor(parts,options){this.parts=parts;this.options=options;}}
class FakeImage{
 constructor(){this.width=640;this.height=480;}
 set src(_){queueMicrotask(()=>this.onload&&this.onload());}
}
const context=vm.createContext({document:doc,URL:fakeURL,Blob:FakeBlob,Image:FakeImage,console,setTimeout});
vm.runInContext(match[1],context);
const run=code=>vm.runInContext(code,context);
const clips={};
for(let c=0;c<10;c++){
 const id="clip_"+String(c).padStart(4,"0");
 clips[id]=Array.from({length:6},(_,frame)=>({
  frame,upper_y:null,lower_y:null,iris_diameter:null,uncertainty_px:null,flags:["UNREVIEWED"]
 }));
}
const template={experiment:"E002-595",rater:"A",arm:"ARM_0",clips};
function fakeFiles(){
 const out=[];
 for(const [clip,rows] of Object.entries(clips))
  for(const row of rows)out.push({
   name:"frame_"+String(row.frame).padStart(2,"0")+".png",
   webkitRelativePath:"ARM_0/clips/"+clip+"/frame_"+String(row.frame).padStart(2,"0")+".png",
   size:1000
  });
 return out;
}
const templateInput=el("template"),imageInput=el("images");
const templateFile=t=>({size:5000,async text(){return JSON.stringify(t);}});
async function tryLoad(t,images){
 templateInput.files=[templateFile(t)];
 imageInput.files=images;
 await run("load()");
 return el("status").textContent;
}
(async()=>{
 const files=fakeFiles();
 assert.equal(files.length,60);
 assert.match(await tryLoad(template,files),/^Verified 60 local PNGs/);
 assert.equal(run("keys.length"),60);
 assert.equal(run('fileKey({webkitRelativePath:"ARM_0/clips/clip_0001/frame_03.png"})'),"clip_0001::3");
 assert.equal(run('fileKey({webkitRelativePath:"ARM_0/owner_mapping.json"})'),null);
 assert.match(await tryLoad(template,files.slice(1)),/^REFUSED: Missing frames/);
 assert.match(await tryLoad(template,[...files,files[0]]),/^REFUSED: Duplicate image mapping/);
 const prefilled=JSON.parse(JSON.stringify(template));
 prefilled.clips.clip_0000[0].upper_y=12;
 assert.match(await tryLoad(prefilled,files),/^REFUSED: Nonblank or malformed template/);
 const wrong=JSON.parse(JSON.stringify(template));wrong.rater="C";
 assert.match(await tryLoad(wrong,files),/^REFUSED: Invalid E002-595 reviewer template/);
 assert.match(await tryLoad(template,files),/^Verified 60 local PNGs/);
 const canvas=el("view");
 canvas._event_click({clientX:320,clientY:200});
 canvas._event_click({clientX:320,clientY:210});
 canvas._event_click({clientX:320,clientY:240});
 el("uncertainty").value="2";
 el("save").onclick();
 assert.equal(run('answers.get(keys[0].key).upper_y'),210);
 assert.equal(run('answers.get(keys[0].key).lower_y'),240);
 assert.equal(run('answers.get(keys[0].key).iris_diameter'),null);
 assert.equal(run('answers.get(keys[0].key).measurement_x'),320);
 el("next").onclick();
 await new Promise(resolve=>setImmediate(resolve));
 el("flag").value="BLUR";
 el("abstain").onclick();
 assert.equal(run('answers.get(keys[1].key).flags[0]'),"BLUR");
 el("export").onclick();
 assert.equal(downloads.length,1);
 assert.equal(downloads[0],"E002_598_A_ARM_0_RATINGS.json");
 const output=JSON.parse(lastBlob.parts.join(""));
 assert.deepEqual(Object.keys(output).sort(),["arm","clips","experiment","rater"]);
 assert.equal(output.clips.clip_0000[0].upper_y,210);
 assert.equal(output.clips.clip_0000[0].iris_diameter,null);
 assert.deepEqual(output.clips.clip_0000[1].flags,["BLUR"]);
 assert.deepEqual(output.clips.clip_0000[2].flags,["UNREVIEWED"]);
 assert(!JSON.stringify(output).includes("participant_id"));
 assert(!JSON.stringify(output).includes("video_sha256"));
 assert(!JSON.stringify(output).includes("native_frame_index"));
 el("clear").onclick();
 assert.equal(run('answers.has(keys[1].key)'),false);
 console.log(JSON.stringify({experiment:"E002-598",status:"SYNTHETIC_UI_TEST_PASS",
  checks:["syntax","no-network/no-storage","60-image source-blind mapping","missing/duplicate refusal",
  "prefilled template refusal","wrong-rater refusal","lid coordinates and uncertainty",
  "nuisance abstention","explicit unreviewed export","no iris-scale fabrication",
  "owner identifiers absent","clear/revert"],human_annotations:0,
  physical_shutter_calibrations:0,product:"ABSTAIN_UNCALIBRATED",release:"BLOCKED"}));
})().catch(e=>{console.error(e);process.exitCode=1;});
