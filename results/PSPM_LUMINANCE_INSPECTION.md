# PsPM-AOB_UW structure inspection

## README

~~~text
PsPM-AOB_UW dataset
=================

Repository Version: 2023.08.16

This dataset includes eye tracker (including pupillometry) measurements from an auditory oddball task with an ITI of 2 s (session 1) and a luminance task in which discs with different shades of grey were presented. Also included are task information, keypress responses, keypress response times and key correctness for the oddball task. Data come from 23 healthy unmedicated female participants aged 41.87 +/- 3.9 years as a control group for a lesion patient with Urbach-Wiethe syndrome. Stimuli consist of sine tones (50-ms length; 10-ms ramp; 440 or 660 Hz).

--------------------------------------------------------------------------------
This repository is curated by the PsPM team, bachlab.org/pspm

--------------------------------------------------------------------------------
Dataset is described and used in following references:
- Abivardi A., Korn C.W., Rojkov I., Gerster S. Hurlemann R., Bach D.R. Acceleration of inferred neural responses to oddball targets in an individual with bilateral amygdala lesion compared to healthy controls. (forthcoming)
--------------------------------------------------------------------------------
File Structure:
-README.txt                        // This document
-+Data                             // Folder Containing all data files
|-AOB_UW_pupil_xx_snY.mat          // 45* files holding measurements for eye tracking
|-AOB__UW_cogent_xx_snY.mat        // 46 files holding key presses and task information

* Pupil data from the luminance task for one participant is missing due to technical failure
-------------------------------------------------------------------------------
Data Files:
- Files holding eyetracking and time markers, recorded with Eyelink software.
  - Pupil left (channel 1) in mm
  - Pupil right (channel 2) in mm
  - Gaze_x left (channel 3)
  - Gaze_y left (channel 4)
  - Gaze_x right (channel 5)
  - Gaze_y right (channel 6)
  - Event markers (channel 7) used for synchronization with Cogent files. See Cogent files for their meaning.
- Files holding:
  - Keyboard presses in response to oddballs (no key presses were required for standards), and task information, recorded with Cogent 2000 software.
  - Screen geometry (screen size, eyetracker distance,w and screen-subject distance in mm) for conversion of gaze coordinates from pixels to mm.

The data file name is composed of:
- AOB_UW       The dataset name
- pupil/cogent The type of data recorded (see above)
- XX           The subject number
- Y            The session number (1: oddball; 2: luminance)

Data are stored as .mat files for use with MATLAB (The MathWorks Inc., Natick, USA) in a format readable by the PsPM toolbox (bachlab.org/pspm). All Matlab files are saved in MATLAB R2022b format.
~~~

Files: 91

## File tree

- Data/AOB_UW_cogent_01_sn1.mat (988 bytes)
- Data/AOB_UW_cogent_01_sn2.mat (765 bytes)
- Data/AOB_UW_cogent_02_sn1.mat (955 bytes)
- Data/AOB_UW_cogent_02_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_03_sn1.mat (956 bytes)
- Data/AOB_UW_cogent_03_sn2.mat (763 bytes)
- Data/AOB_UW_cogent_04_sn1.mat (963 bytes)
- Data/AOB_UW_cogent_04_sn2.mat (765 bytes)
- Data/AOB_UW_cogent_05_sn1.mat (965 bytes)
- Data/AOB_UW_cogent_05_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_06_sn1.mat (969 bytes)
- Data/AOB_UW_cogent_06_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_07_sn1.mat (951 bytes)
- Data/AOB_UW_cogent_07_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_08_sn1.mat (946 bytes)
- Data/AOB_UW_cogent_08_sn2.mat (763 bytes)
- Data/AOB_UW_cogent_09_sn1.mat (956 bytes)
- Data/AOB_UW_cogent_09_sn2.mat (758 bytes)
- Data/AOB_UW_cogent_10_sn1.mat (959 bytes)
- Data/AOB_UW_cogent_10_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_11_sn1.mat (970 bytes)
- Data/AOB_UW_cogent_11_sn2.mat (758 bytes)
- Data/AOB_UW_cogent_12_sn1.mat (951 bytes)
- Data/AOB_UW_cogent_12_sn2.mat (757 bytes)
- Data/AOB_UW_cogent_13_sn1.mat (957 bytes)
- Data/AOB_UW_cogent_13_sn2.mat (759 bytes)
- Data/AOB_UW_cogent_14_sn1.mat (961 bytes)
- Data/AOB_UW_cogent_14_sn2.mat (757 bytes)
- Data/AOB_UW_cogent_15_sn1.mat (952 bytes)
- Data/AOB_UW_cogent_15_sn2.mat (760 bytes)
- Data/AOB_UW_cogent_16_sn1.mat (958 bytes)
- Data/AOB_UW_cogent_16_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_17_sn1.mat (954 bytes)
- Data/AOB_UW_cogent_17_sn2.mat (765 bytes)
- Data/AOB_UW_cogent_18_sn1.mat (963 bytes)
- Data/AOB_UW_cogent_18_sn2.mat (760 bytes)
- Data/AOB_UW_cogent_19_sn1.mat (951 bytes)
- Data/AOB_UW_cogent_19_sn2.mat (762 bytes)
- Data/AOB_UW_cogent_20_sn1.mat (951 bytes)
- Data/AOB_UW_cogent_20_sn2.mat (761 bytes)
- Data/AOB_UW_cogent_21_sn1.mat (952 bytes)
- Data/AOB_UW_cogent_21_sn2.mat (764 bytes)
- Data/AOB_UW_cogent_22_sn1.mat (952 bytes)
- Data/AOB_UW_cogent_22_sn2.mat (759 bytes)
- Data/AOB_UW_cogent_23_sn1.mat (963 bytes)
- Data/AOB_UW_cogent_23_sn2.mat (761 bytes)
- Data/AOB_UW_pupil_01_sn1.mat (2,365,609 bytes)
- Data/AOB_UW_pupil_01_sn2.mat (1,713,611 bytes)
- Data/AOB_UW_pupil_02_sn1.mat (2,670,331 bytes)
- Data/AOB_UW_pupil_02_sn2.mat (1,947,584 bytes)
- Data/AOB_UW_pupil_03_sn1.mat (2,224,176 bytes)
- Data/AOB_UW_pupil_03_sn2.mat (1,648,433 bytes)
- Data/AOB_UW_pupil_04_sn1.mat (2,601,003 bytes)
- Data/AOB_UW_pupil_04_sn2.mat (2,047,522 bytes)
- Data/AOB_UW_pupil_05_sn1.mat (2,798,196 bytes)
- Data/AOB_UW_pupil_05_sn2.mat (1,965,858 bytes)
- Data/AOB_UW_pupil_06_sn1.mat (2,603,096 bytes)
- Data/AOB_UW_pupil_07_sn1.mat (2,532,494 bytes)
- Data/AOB_UW_pupil_07_sn2.mat (1,766,268 bytes)
- Data/AOB_UW_pupil_08_sn1.mat (2,763,057 bytes)
- Data/AOB_UW_pupil_08_sn2.mat (1,983,737 bytes)
- Data/AOB_UW_pupil_09_sn1.mat (2,641,133 bytes)
- Data/AOB_UW_pupil_09_sn2.mat (1,745,520 bytes)
- Data/AOB_UW_pupil_10_sn1.mat (2,318,782 bytes)
- Data/AOB_UW_pupil_10_sn2.mat (1,709,967 bytes)
- Data/AOB_UW_pupil_11_sn1.mat (1,854,279 bytes)
- Data/AOB_UW_pupil_11_sn2.mat (1,876,227 bytes)
- Data/AOB_UW_pupil_12_sn1.mat (2,702,949 bytes)
- Data/AOB_UW_pupil_12_sn2.mat (1,848,158 bytes)
- Data/AOB_UW_pupil_13_sn1.mat (2,464,364 bytes)
- Data/AOB_UW_pupil_13_sn2.mat (1,841,274 bytes)
- Data/AOB_UW_pupil_14_sn1.mat (2,958,401 bytes)
- Data/AOB_UW_pupil_14_sn2.mat (1,670,955 bytes)
- Data/AOB_UW_pupil_15_sn1.mat (2,754,639 bytes)
- Data/AOB_UW_pupil_15_sn2.mat (1,967,984 bytes)
- Data/AOB_UW_pupil_16_sn1.mat (2,596,911 bytes)
- Data/AOB_UW_pupil_16_sn2.mat (1,926,691 bytes)
- Data/AOB_UW_pupil_17_sn1.mat (2,803,602 bytes)
- Data/AOB_UW_pupil_17_sn2.mat (2,072,047 bytes)
- Data/AOB_UW_pupil_18_sn1.mat (2,486,243 bytes)
- Data/AOB_UW_pupil_18_sn2.mat (1,847,741 bytes)
- Data/AOB_UW_pupil_19_sn1.mat (2,526,864 bytes)
- Data/AOB_UW_pupil_19_sn2.mat (1,963,576 bytes)
- Data/AOB_UW_pupil_20_sn1.mat (2,663,700 bytes)
- Data/AOB_UW_pupil_20_sn2.mat (1,876,923 bytes)
- Data/AOB_UW_pupil_21_sn1.mat (2,612,779 bytes)
- Data/AOB_UW_pupil_21_sn2.mat (1,693,151 bytes)
- Data/AOB_UW_pupil_22_sn1.mat (2,602,180 bytes)
- Data/AOB_UW_pupil_22_sn2.mat (1,957,326 bytes)
- Data/AOB_UW_pupil_23_sn1.mat (2,414,717 bytes)
- Data/AOB_UW_pupil_23_sn2.mat (1,840,836 bytes)