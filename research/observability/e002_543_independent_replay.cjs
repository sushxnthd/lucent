#!/usr/bin/env node
'use strict';
// E002-543 independent arithmetic: does not import Python or reuse its evaluator.
const assert = require('node:assert/strict');
function classify(pulse, shutter, uncertainty, control, flash, noise) {
  const outside = (pulse[3] + uncertainty < shutter[0]) ||
                  (pulse[0] - uncertainty > shutter[3]);
  if (!outside) return 'ABSTAIN_NOT_OUTSIDE';
  return Math.abs(flash - control) > noise ?
    'TRANSFER_FALSIFICATION_CANDIDATE' : 'NO_FALSIFICATION_CENSORED';
}
// pulse=[earliest onset,latest onset,earliest offset,latest offset];
// shutter=[earliest start,latest start,earliest end,latest end].
const shutter=[3,3.1,5,5.1];
assert.equal(classify([0,.1,.9,1],shutter,.2,.2,.8,.05), 'TRANSFER_FALSIFICATION_CANDIDATE');
assert.equal(classify([7,7.1,8,8.1],shutter,.2,.2,.23,.05), 'NO_FALSIFICATION_CENSORED');
assert.equal(classify([4,4.1,4.5,4.6],shutter,.2,.2,.8,.05), 'ABSTAIN_NOT_OUTSIDE');
assert.equal(classify([0,.1,.9,1],shutter,2.1,.2,.8,.05), 'ABSTAIN_NOT_OUTSIDE');
assert.equal(classify([0,.1,2.9,3],shutter,0,.2,.8,.05), 'ABSTAIN_NOT_OUTSIDE');
assert.equal(classify([0,.1,.9,1],shutter,.2,.2,.25,.05), 'NO_FALSIFICATION_CENSORED');
console.log('E002-543 independent replay: six strict-boundary and censoring checks passed; synthetic only');
