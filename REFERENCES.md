# Literature and Benchmark Map

This is a working map of the literature that motivates Lucent's measurement and validation choices. Inclusion does not imply that Lucent reproduces or endorses every result.

## Reference measurements

### Psychomotor vigilance

**Dinges, D. F. & Powell, J. W. (1985).**  
*Microcomputer analyses of performance on a portable, simple visual RT task during sustained operations.*  
Behavior Research Methods, Instruments, & Computers, 17(6), 652-655.  
https://doi.org/10.3758/BF03200977

Why it matters: reaction-time / vigilance measures provide an objective behavioral target sensitive to sleep loss and sustained-performance degradation.

### State sleepiness

**Kaida, K. et al. (2006).**  
*Validation of the Karolinska sleepiness scale against performance and EEG variables.*  
Clinical Neurophysiology, 117(7), 1574-1581.  
https://doi.org/10.1016/j.clinph.2006.03.011

Why it matters: subjective state sleepiness should be treated as a useful target, but not as interchangeable with behavioral performance.

## Visual fatigue / drowsiness signals

### PERCLOS

**Wierwille and colleagues / U.S. DOT evaluation work.**  
PERCLOS measures the percentage of time the eyes are substantially closed and became a classic ocular alertness measure.  
https://rosap.ntl.bts.gov/view/dot/113

Why it matters: ocular dynamics are a strong historical reason to test temporal eye-region information, while avoiding the assumption that one feature fully captures cognitive state.

## Public datasets

### DROZY

**Massoz, Q., Langohr, T., François, C. et al. (2016).**  
*The ULg Multimodality Drowsiness Database (called DROZY) and examples of use.*  
IEEE Winter Conference on Applications of Computer Vision.  
https://doi.org/10.1109/WACV.2016.7477715

DROZY includes video alongside physiological and drowsiness-related measurements and is useful for pipeline prototyping and multimodal comparison.

Dataset: https://www.drozy.uliege.be/

### UTA Real-Life Drowsiness Dataset (RLDD)

**Ghoddoosian, R., Galib, M. & Athitsos, V. (2019).**  
*A Realistic Dataset and Baseline Temporal Model for Early Drowsiness Detection.*  
CVPR Workshops.

Paper: https://openaccess.thecvf.com/content_CVPRW_2019/html/AMFG/Ghoddoosian_A_Realistic_Dataset_and_Baseline_Temporal_Model_for_Early_Drowsiness_CVPRW_2019_paper.html  
Dataset: https://sites.google.com/view/utarldd/home

Why it matters: RGB video recorded across participants and natural variation is useful for representation and robustness experiments, though class labels are not a substitute for Lucent's intended paired behavioral targets.

## Important distinction

Driver-drowsiness classification and Lucent's target are not the same problem.

Lucent is interested in whether **brief commodity video can recover a continuous or person-relative state signal that predicts contemporaneous cognitive performance**, under participant-held-out evaluation. Existing drowsiness datasets are useful as supporting benchmarks, not definitive validation of that thesis.
