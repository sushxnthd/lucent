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

## Novelty statement

Two literature searches conducted for Lucent did **not** locate a study jointly combining:

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
