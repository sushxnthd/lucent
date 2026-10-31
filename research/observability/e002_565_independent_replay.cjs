'use strict';
// Independent Node.js implementation of the frozen source-identity join.
const assert = require('node:assert/strict');
const R = {
  '18970793': ['motor_imagery','MI','fb56109542a13aa7879778833fe4cbaa'],
  '18971758': ['motor_execution','ME','bce89dd9fbb67e27a656623aa27927e0']
};
const keys = ['zenodo_record','paradigm','archive_md5','video_member','session','participant_id','video_sha256','frame_namespace'];
function valid(x) {
  if (!x || typeof x !== 'object' || Array.isArray(x) || keys.some(k => typeof x[k] !== 'string')) return false;
  const r = R[x.zenodo_record];
  if (!r || x.paradigm !== r[0] || x.archive_md5 !== r[2]) return false;
  if (!/^[a-f0-9]{64}$/.test(x.video_sha256) || !/^S\d{2}$/.test(x.participant_id) || !/^Sess\d{2}$/.test(x.session)) return false;
  const re = new RegExp('^'+x.session+'/'+r[1]+'[0-9]{3}_phantom\\.avi$');
  return re.test(x.video_member) && x.frame_namespace === 'native-index:'+x.video_member.split('/').at(-1);
}
function verdict(a,b) {
  if (!valid(a) || !valid(b)) return 'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE';
  if (a.paradigm !== b.paradigm || a.zenodo_record !== b.zenodo_record) return 'REJECT_CROSS_PARADIGM';
  if (a.video_sha256 !== b.video_sha256) return 'REJECT_VIDEO_IDENTITY';
  if (['video_member','session','participant_id','frame_namespace'].some(k=>a[k]!==b[k])) return 'REJECT_SAMPLE_NAMESPACE';
  return 'SOURCE_MATCH_ONLY_UNCALIBRATED';
}
function source(record='18970793') {
  const mi=record==='18970793', stem=mi?'MI011':'ME011';
  return {zenodo_record:record,paradigm:mi?'motor_imagery':'motor_execution',
    archive_md5:mi?R['18970793'][2]:R['18971758'][2],video_member:'Sess01/'+stem+'_phantom.avi',
    session:'Sess01',participant_id:'S01',video_sha256:'a'.repeat(64),frame_namespace:'native-index:'+stem+'_phantom.avi'};
}
const cases=[];
let a=source(),b=source(); cases.push([a,b,'SOURCE_MATCH_ONLY_UNCALIBRATED']);
cases.push([source(),source('18971758'),'REJECT_CROSS_PARADIGM']);
b=source();b.video_sha256='b'.repeat(64);cases.push([source(),b,'REJECT_VIDEO_IDENTITY']);
b=source();b.session='Sess02';b.video_member='Sess02/MI011_phantom.avi';cases.push([source(),b,'REJECT_SAMPLE_NAMESPACE']);
b=source();b.archive_md5='0'.repeat(32);cases.push([source(),b,'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE']);
b=source();delete b.video_sha256;cases.push([source(),b,'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE']);
b=source();b.video_member='Sess01/MI012_phantom.avi';b.frame_namespace='native-index:MI012_phantom.avi';cases.push([source(),b,'REJECT_SAMPLE_NAMESPACE']);
b=source();b.paradigm='motor_execution';cases.push([source(),b,'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE']);
for (const [a,b,expected] of cases) assert.equal(verdict(a,b),expected);
console.log(JSON.stringify({experiment:'E002-565',independent_node_cases:cases.length,disagreements:0,physical_validation:false,release:'BLOCKED'}));
