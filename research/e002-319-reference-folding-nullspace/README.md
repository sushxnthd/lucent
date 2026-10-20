# Lucent E002-319

Source-specific conditional result: EyeDentify's published 90-Hz Tobii to 30-fps webcam preprocessing averages corresponding rows from three one-second blocks, not adjacent samples. For exactly 90 samples per second, y[j]=(x[j]+x[j+90]+x[j+180])/3. The operator has rank 90, nullity 180, and an exact 1/3-Hz temporal null; session mean survives. No human data was analyzed. This is not an impossibility result about the RGB camera itself.
