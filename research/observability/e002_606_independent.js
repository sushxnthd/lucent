'use strict';
// Independent finite-grid enumeration, not a call to Python or its formula.
const gcd=(a,b)=>{while(b){const t=a%b;a=b;b=t;}return a;};
const lcm=(a,b)=>a/gcd(a,b)*b;
function misses(high,low,bins){
  const tick=lcm(high,low),period=tick/low,width=bins*(tick/high);
  let missed=0;
  for(let phase=0;phase<period;phase++){
    let seen=false;
    for(let k=-1;k<=Math.floor(width/period)+1;k++){
      const t=phase+k*period;
      if(t>=0&&t<width)seen=true;
    }
    if(!seen)missed++;
  }
  const d=gcd(missed,period);
  return `${missed/d}/${period/d}`;
}
const expected={'100:1':'7/10','100:2':'2/5','100:3':'1/10','100:4':'0/1',
                '110:1':'8/11','110:2':'5/11','110:3':'2/11','110:4':'0/1'};
for(const [key,want] of Object.entries(expected)){
  const [high,bins]=key.split(':').map(Number);
  const got=misses(high,30,bins);
  if(got!==want)throw new Error(`${key}: ${got} != ${want}`);
}
console.log(JSON.stringify({experiment:'E002-606',independent_js_lattice_cases:8,pass:true}));
