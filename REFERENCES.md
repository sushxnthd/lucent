# Literature and Novelty Map

This is a working map of the literature that bounds Lucent / APST-5. Inclusion does not imply that Lucent reproduces or endorses every result.

## Active probing and experiment design

### Salti, Be'ery & Aluf (2022)
*An active approach towards monitoring and enhancing drivers' capabilities — the ADAM cogtec solution.*  
https://doi.org/10.48550/arXiv.2204.10853

Why it matters: active ocular probing for transient impairment already exists. Lucent therefore cannot claim novelty for "active probing" itself. The gap is ultra-short smartphone execution plus explicit probe optimization and longitudinal state inference.

### Lewi, Butera & Paninski (2006)
*Real-time adaptive information-theoretic optimization of neurophysiology experiments.*  
https://doi.org/10.7551/mitpress/7503.003.0112

Why it matters: information-theoretic stimulus selection is established methodology. APST-5 applies that logic to a constrained smartphone human-state probe.

## Pupil system identification

### Zénon (2017)
*Time-domain analysis for extracting fast-paced pupil responses.*  
https://doi.org/10.1038/srep41484

Why it matters: demonstrates ARX system identification for rapid pupil responses and strong subject-specific differences in response amplitude and latency.

### Korn & Bach (2016)
*A solid frame for the window on cognition: Modelling event-related pupil responses.*  
https://doi.org/10.1167/16.3.28

Why it matters: provides a forward dynamical view of luminance and non-luminance pupil responses.

## Public controlled-luminance calibration datasets

### PsPM-AOB_UW public dataset

Zenodo: https://doi.org/10.5281/zenodo.8239465

Why it matters: provides repeated controlled screen-luminance transitions with 500 Hz left/right pupil diameter in millimeters. Lucent uses the released luminance recording to replace the hand-specified pupil-response surrogate with participant-specific empirical response functions in APST5-HUMAN-PRF-001.

The preregistered single-kernel probe test failed. A predeclared post-primary brightening/darkening analysis selected the already frozen E002 timing on the design participants and exceeded its engineering separation threshold on held-out participants. That secondary result is kept separate from the failed primary.

### Ehinger et al. Eye Tracking Comparison dataset

Code: https://github.com/behinger/etcomp  
Figshare collection: https://doi.org/10.6084/m9.figshare.c.4379810.v1

Why it matters: provides concurrent EyeLink 1000 and Pupil Labs recordings during a controlled display-luminance task. EHINGER-DEVICE-TRANSFER-001 uses blocks 1–3 for device calibration and blocks 4–6 for held-out evaluation.

The preregistered cross-device waveform criterion passed (macro-r 0.9974, 95% CI [0.9948,0.9987], 15/15 participant r>0.70). A secondary leave-one-person-out residual test also found person-specific cross-device agreement beyond mismatched-participant controls. Pupil Labs remains a dedicated eye tracker rather than an ordinary phone front camera.

## Screen-driven pupil response and state sensitivity

### Wang et al. (2018)
*Pupil light reflex evoked by light-emitting diode and computer screen: Methodology and association with need for recovery in daily life.*  
https://doi.org/10.1371/journal.pone.0197739

Why it matters: establishes that a display can drive measurable pupil-light-reflex dynamics and reports associations with need for recovery.

### Pan et al. (2022)
*Arousal-based pupil modulation is dictated by luminance.*  
https://doi.org/10.1038/s41598-022-05280-1

Why it matters: state sensitivity changes with luminance, motivating stimulus design rather than simply maximizing screen brightness.

### Podolak et al. (2019)
*The utility of pupillary light reflex as an objective biomarker of acute concussion in the adolescent athlete.*  
https://doi.org/10.1177/2325967119S00155

Why it matters: a 0.8-second light input with a 5-second recording window demonstrates that clinically meaningful PLR dynamics can fit inside the same overall time budget, although the target and hardware differ from Lucent.

## Five-second passive baseline

### Massoz, Verly & Van Droogenbroeck (2018)
*Multi-Timescale Drowsiness Characterization Based on a Video of a Driver's Face.*  
https://doi.org/10.3390/s18092801

Why it matters: five-second passive face video is already a serious baseline. Their five-second branch achieved lower performance than longer windows, creating the temporal-compression problem APST-5 tries to attack with active measurement.

## Smartphone pupillometry

### Barry et al. (2022)
*At-Home Pupillometry using Smartphone Facial Identification Cameras.*  
https://doi.org/10.1145/3491102.3502493

Why it matters: validates smartphone-based pupil tracking and a phone-driven pupil-light-reflex test, while also exposing camera, eye-color, movement, and sensor limitations relevant to APST-5.

## Temporal representation and protocol limits

### Zhang (2026)
*The Label Defines the Timescale: Trait-State Limits of Temporal-Aggregate Learning.*  
https://arxiv.org/abs/2608.01587

Why it matters: derives protocol-conditioned Bayes-risk limits showing that label construction and latent temporal dynamics jointly determine the useful observation span. This precludes a broad novelty claim that Lucent originated the idea that "the label defines the timescale." Lucent's narrower contribution is the controlled empirical target-history interaction and its replication/falsification record.

### Gagnon et al. (2016)
*A Systematic Assessment of Operational Metrics for Modeling Operator Functional State.*  
https://doi.org/10.5220/0005921600150023

Why it matters: shows that the smoothing window used to construct performance labels materially affects physiological-model performance.

### Smith, Clark & Endsley (2025)
*Balancing temporal dynamics with measurement noise in real-time situation awareness prediction.*  
https://doi.org/10.1080/00140139.2025.2558703

Why it matters: demonstrates that short moving-average behavioral targets can reduce measurement noise and become more predictable from physiological signals.

### Yamashita et al. (2021)
*Pupillary fluctuation amplitude before target presentation reflects short-term vigilance level in Psychomotor Vigilance Tasks.*  
https://doi.org/10.1371/journal.pone.0256953

Why it matters: reports that approximately one-to-two seconds of pre-target pupil fluctuation is informative about trial-level PVT reaction time, providing a close precedent for ultra-short passive vigilance sensing.

### Martin, Whittaker & Johnston (2022)
*Pupillometry and the vigilance decrement: Task-evoked but not baseline pupil measures reflect declining performance in visual vigilance tasks.*  
https://doi.org/10.1111/ejn.15585

Raw Experiment 2 data: https://doi.org/10.6084/m9.figshare.17317886.v1

Why it matters: provides an independent 25-participant, 250 Hz EyeLink PVT dataset used for MARTIN-PVT-TARGET-ALIGNMENT-001.

## Active perturbation as a general measurement principle

### Truslow et al. (2026)
*External conditioning of data collection enhances the information content from wearable sensors.*  
https://doi.org/10.1038/s44325-026-00144-3

Why it matters: a one-minute Apple Watch mindful-breathing perturbation increased the discriminative information in HRV for seven cardiometabolic disease targets, whereas passive timing/sleep contexts did not. This is strong prior art for the **general principle** that structured active perturbations can make wearable physiology more informative. Lucent therefore cannot claim novelty for active perturbation itself; the open gap is the specific ultra-short display-controlled ocular system-identification setting.

## Novelty statement

Multiple literature searches conducted for Lucent did **not** locate a study jointly combining:

- an ordinary smartphone;
- a strict approximately five-second active scan;
- display-controlled stimulus design;
- synchronized ocular / facial camera response;
- explicit Fisher-information or mutual-information optimization of the probe;
- personal longitudinal priors;
- paired behavioral state targets;
- unseen-participant and unseen-device validation.

This is the current defensible novelty gap. It should be treated as a search result, not as proof of universal priority.


## Combined oculomotor fatigue screens

### Mulligan, Díaz-Piedra & Di Stasi (2017)
*Oculomotor Assessment of Diurnal Arousal Variations.*  
https://doi.org/10.1167/17.10.1153

Why it matters: a 30-second automated test combined saccadic peak velocity, pupil diameter, PLR latency, and PLR amplitude. This is the strongest short combined fatigue-screen precedent located so far.

### Rowland et al. (2005)
*Oculomotor responses during partial and total sleep deprivation.*  
https://www.semanticscholar.org/paper/1c24379983403a537069bf344eb4388ac5ea0f55

Why it matters: a 45-second automated oculomotor test found increased pupil-constriction latency and decreased saccadic velocity during total sleep deprivation.

### McClelland, Pilcher & Moore (2010)
*Oculomotor measures as predictors of performance during sleep deprivation.*  
https://doi.org/10.3357/ASEM.2653.2010

Why it matters: pupil diameter, constriction latency, and saccadic velocity predicted PVT performance under sleep deprivation.

### Chen et al. (2022)
*Fatigue and Arousal Modulations Revealed by Saccade and Pupil Dynamics.*  
https://doi.org/10.3390/ijerph19159234

Why it matters: fatigue / time-on-task affected both pupil and saccade dynamics, supporting a multimodal rather than single-feature state probe.

### Lai et al. (2020)
*Measuring Saccade Latency Using Smartphone Cameras.*  
https://doi.org/10.1109/JBHI.2019.2913846

Why it matters: establishes smartphone-camera oculomotor measurement, but at much longer effective measurement duration than Lucent's target.

See [docs/MULTIMODAL_COMPRESSION.md](docs/MULTIMODAL_COMPRESSION.md) for the current temporal-compression boundary.
