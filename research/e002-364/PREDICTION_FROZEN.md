# Frozen synthetic predictions (before independent verification)
F=100/3 ms, w=10 ms, G=20 ms, rows [0,d/2,d] ms, rho_i=1, global L2 epsilon=.12.
- d=0: H=23.333333 ms; exact blind gap exists.
- d=8: H=15.333333 ms; G=20 is not completely invisible.
- d=6.5: worst-phase separation ~0.223917 <0.24; bounded-noise failure.
- d=7: worst-phase separation ~0.259272 >0.24; bounded-noise success.
- local critical span d*=6.727445883 ms; noiseless span threshold 3.333333 ms.
- d=8 with +/-0.5-ms independent row clock errors: robust H=16.333333 ms, allowing a 16-ms gap collision.
- d=8, 14-ms opening between two 120-ms closures: byte-identical synthetic RGB vs 254-ms merged closure, although simulated 500-fps reference distinguishes.
Synthetic only. This is NOT an unseen human prediction.
Original freeze SHA256 8f84a3c617a98846ba9031635eccfeac7fdf78f26c18a09b0e88884b06d1dd1c in local archive.