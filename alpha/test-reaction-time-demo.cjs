// Dependency-free deterministic behavioral regression for alpha/reaction-time-demo.html.
// Run: node alpha/test-reaction-time-demo.cjs
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(require('node:path').join(__dirname, 'reaction-time-demo.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'inline application script must exist');
function harness() {
  const elements = new Map();
  const listeners = {};
  for (const id of ['start','reset','target','status','result','self','export']) {
    elements.set('#'+id, {id, value:'4', disabled:id==='target'||id==='export', textContent:'', className:'', listeners:{}, addEventListener(event,fn){this.listeners[event]=fn}, click(){if(!this.disabled)this.listeners.click?.()}});
  }
  let now=0, seq=0, tasks=new Map(), hidden=false, downloads=0;
  const document={querySelector: id=>elements.get(id), get hidden(){return hidden}, addEventListener:(event,fn)=>listeners[event]=fn, createElement:()=>({click(){downloads++}})};
  const window={addEventListener:(event,fn)=>listeners[event]=fn};
  const URL={createObjectURL:()=> 'blob:test', revokeObjectURL:()=>{}};
  const context={document,window,URL,Blob,Math,JSON,Number,performance:{now:()=>now},setTimeout:(fn,delay)=>{const id=++seq;tasks.set(id,{at:now+delay,fn});return id},clearTimeout:id=>tasks.delete(id)};
  vm.runInNewContext(script,context,{timeout:1000});
  function advance(ms){const until=now+ms;let limit=0;while(true){const pending=[...tasks].sort((a,b)=>a[1].at-b[1].at)[0];if(!pending||pending[1].at>until)break;assert.ok(++limit<100,'timer loop');now=pending[1].at;tasks.delete(pending[0]);pending[1].fn()}now=until}
  return {e:id=>elements.get('#'+id),advance,blur:()=>listeners.blur?.(),hide:()=>{hidden=true;listeners.visibilitychange?.()},get downloads(){return downloads}};
}
function finish(h){h.e('start').click();for(let i=0;i<5;i++){h.advance(4100);assert.equal(h.e('target').disabled,false);h.e('target').click();if(i<4)h.advance(900)}}
{
 const h=harness();finish(h);
 assert.match(h.e('status').textContent,/complete/);
 assert.match(h.e('result').textContent,/No fatigue classification/);
 assert.equal(h.e('export').disabled,false);
 h.e('export').click();assert.equal(h.downloads,1);
 h.e('reset').click();assert.equal(h.e('export').disabled,true);
}
{
 const h=harness();h.e('start').click();h.e('target').click();assert.match(h.e('status').textContent,/Early tap/);
 h.blur();h.advance(10000);assert.match(h.e('status').textContent,/Focus lost/);assert.equal(h.e('export').disabled,true);
}
{
 const h=harness();h.e('start').click();h.hide();h.advance(10000);assert.match(h.e('status').textContent,/interrupted/);assert.equal(h.e('export').disabled,true);
}
{
 const h=harness();h.e('start').click();h.advance(4100);h.advance(11000);h.e('target').click();
 assert.match(h.e('status').textContent,/Invalid or excessively delayed/);
 assert.equal(h.e('export').disabled,true);
}
console.log('PASS: completion/export/reset, early-tap blur, visibility interruption, delayed-response invalidation');
