# Eye-BCI Phantom/Tobii alignment audit

## Phantom mapping

sync rows: **363,040**
rows with PhanFrame: **51,252**
PhanFrame range: **166.0 .. 51417.0**
Time range at mapped frames: **18.796000 .. 351.571000 s**

- PhanFrame: finite=51,252, min=166.0, max=51417.0
- PhanTime: finite=0, min=nan, max=nan
- RelTime: finite=51,252, min=0.0, max=332772.0
- RecordingTimestamp: finite=40, min=53110.0, max=358055.0
- LocalTimeStamp: finite=0, min=nan, max=nan

first mapped rows:

    Time,PhanFrame,PhanTime,RelTime,RecordingTimestamp,LocalTimeStamp
    18.796,166.0,09:32:52.409 169.52,0.0,,
    18.802,167.0,09:32:52.415 556.96,6.0,,
    18.809,168.0,09:32:52.421 910.93,12.0,,
    18.815,169.0,09:32:52.428 279.79,19.0,,
    18.821,170.0,09:32:52.434 633.75,25.0,,
    18.828,171.0,09:32:52.440 961.77,31.0,,
    18.834,172.0,09:32:52.447 329.48,38.0,,
    18.841,173.0,09:32:52.453 880.50,44.0,,
    18.847,174.0,09:32:52.460 279.07,51.0,,
    18.853,175.0,09:32:52.466 569.86,57.0,,
    18.86,176.0,09:32:52.472 990.75,63.0,,
    18.866,177.0,09:32:52.479 336.16,70.0,,
    

## Tobii pupil stream

Tobii rows: **115,041**
rows with pupil: **42,799**
RecordingTimestamp range: **17724 .. 371834 ms**
PupilLeft range: **1.44 .. 4.01**
PupilRight range: **1.4 .. 4.16**

first valid pupil rows:

    RecordingTimestamp,LocalTimeStamp,PupilLeft,PupilRight,ValidityLeft,ValidityRight,CamLeftX,CamLeftY,CamRightX,CamRightY
    17724,17:57:17.082,3.42,3.43,3.0,1.0,,,,
    17727,17:57:17.085,3.42,3.43,3.0,1.0,,,,
    17731,17:57:17.089,3.37,3.38,3.0,1.0,,,,
    17734,17:57:17.092,3.43,3.43,3.0,1.0,,,,
    17737,17:57:17.095,3.29,3.29,3.0,1.0,,,,
    17741,17:57:17.098,3.23,3.23,3.0,1.0,,,,
    17744,17:57:17.102,3.3,3.3,3.0,1.0,,,,
    17747,17:57:17.105,3.35,3.35,3.0,1.0,,,,
    17751,17:57:17.109,3.44,3.45,3.0,1.0,,,,
    17754,17:57:17.112,3.32,3.33,3.0,1.0,,,,
    17757,17:57:17.115,3.33,3.32,3.0,1.0,,,,
    17761,17:57:17.118,3.26,3.26,3.0,1.0,,,,
    

## Timestamp compatibility

raw RecordingTimestamp overlap: **53110.0 .. 358055.0**
overlap exists: **True**
Tobii median timestamp step: **3.000**