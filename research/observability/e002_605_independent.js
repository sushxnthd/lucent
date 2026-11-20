'use strict';
// Independent integer enumeration, not a translation of Python's modular shortcut.
function missed(lo,hi){
 let n=0;
 for(let phase=0;phase<3;phase++){
   let observed=false;
   for(let frame=lo;frame<=hi;frame++)if(frame%3===phase){observed=true;break;}
   if(!observed)n++;
 }
 return n;
}
for(let start=0;start<100;start++){
 for(const [width,expected] of [[1,2],[2,1],[3,0],[4,0],[11,0]]){
  if(missed(start,start+width-1)!==expected)throw new Error('phase law failure');
 }
}
console.log(JSON.stringify({experiment:'E002-605',independent_integer_phase_checks:500,pass:true}));
