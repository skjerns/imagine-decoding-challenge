# imagine-decoding-challenge

The epochs have been scrambled! Can you figure out in which epoch we played which auditory word by training a visual decoder *on images of the words*?

<img width="600" alt="Clipboard_10-14-2025_01" src="https://github.com/user-attachments/assets/6edcd445-7b4f-44cd-8bfc-5562d6c58375" />

You can win a total of 1000$ in price money!

Direct link to the Kaggle competition: https://www.kaggle.com/competitions/the-imagine-decoding-challenge

## Overview

Can you decode which images people were thinking of from data recorded while they were visually seeing these images?

In memory research, decoders are often trained on localizer data to extract neural activation patterns of specific stimuli (e.g., “what pattern occurs when we see a clown”). Taken as evidence for reprocessing, these decoders are then used to detect pattern presence in other parts of the experiment (e.g., “after learning something about clowns, we can see the activation pattern of ‘clown’ being more active than expected; that means knowledge is being consolidated”). But how well does this actually work?  

We recorded a simple paradigm in the [Magnetoencephalograph (MEG)](https://en.wikipedia.org/wiki/Magnetoencephalography) in which we showed [ten different visual items](https://github.com/skjerns/imagine-decoding-challenge/blob/main/md_assets/stimuli.png) many times to participants. Later, we played back spoken words describing the items while they had their eyes closed and asked them to mentally visualize the items associated with the word as vividly as possible. Can you train a decoder on the visual presentation (`localizer`) and decode which item people imagined?

## Experiment

We recorded a **localizer** in the [MEG](https://en.wikipedia.org/wiki/Magnetoencephalography) with 30 participants, presenting one of [ten different items](https://github.com/skjerns/imagine-decoding-challenge/blob/main/md_assets/stimuli.png) in random order. [In each trial](md_assets/diagram_localizer.png), participants first heard a word describing the item (e.g., “clown”) for ~1 second, then saw an image that either matched (i.e., was a clown) or did not, in which case they had to press a button. After that, they performed the study reported in Kern et al. ([2024](https://elifesciences.org/articles/93357) & [2025](https://elifesciences.org/reviewed-preprints/108023)), which is not of interest right now. Directly after the main experiment ended, [they closed their eyes](md_assets/diagram_imagine.png) and once again **heard the words** describing the stimuli. They were asked to **imagine the cued image** as vividly as possible whenever they heard its word.

**Goal:** The epochs have been scrambled! Can you figure out in which epoch we played which word as an auditory stimulus by training a decoder on visual images of the words?

Example of the localizer trials (tip: unmute audio).  
Instructions: *“Press a button if there is a mismatch between word and image.”*

https://github.com/user-attachments/assets/d093c932-83a1-435b-920a-1e89369ac48d

Example of the imagine trials (tip: unmute audio).  
Instructions: *“Close your eyes and mentally imagine the image belonging to the word you hear as vividly as possible.”*

https://github.com/user-attachments/assets/7a6b6ba3-c3f0-4c2f-ace2-3a9cb33e2a62

See a schematic of the two trial types here: [trial schematic](md_assets/diagram_trials.png)

## The Data

The data consist of `mne.Epochs` from the `localizer` and `imagine` trials. The data were preprocessed with [tSSS MaxFilter](https://imaging.mrc-cbu.cam.ac.uk/meg/Maxfilter) and resampled to 100 Hz. Continuous HPI was recorded and used to realign head position to the mean position in the localizer. No alignment between participants was performed, so sensor positions may capture slightly different brain areas. Epochs are aligned with the visual stimulus onset (`localizer`) or word onset (`imagine`). The `localizer` epochs were intentionally truncated and baseline-corrected to remove the word-processing signal before visual onset. No other preprocessing was applied, which depending on who you ask is either [not necessary](https://www.nature.com/articles/s41598-023-27528-0) or [potentially useful](https://www.nature.com/articles/s42003-025-08464-3). We recorded 306 MEG channels on a MEGIN Triux system, including 102 magnetometers and 204 planar gradiometers ([Vectorview layout](https://mne.tools/stable/generated/mne.channels.Layout.html#mne-channels-layout)). Additionally, ECG and horizontal and vertical EOG were recorded.

**Localizer:** 480 epochs, 48 per stimulus item. Each trial spans −200 ms before visual onset to 1000 ms after onset. Trials with mismatched word–image pairs were removed. Baseline correction used the pre-onset interval. Each trial has a label corresponding to one of the stimuli.

**Imagine:** Epochs span −200 ms to 5000 ms after word onset, with no baseline correction. There are 20–50 epochs per participant, with 3–5 trials per stimulus. Trial labels were removed and replaced by numbers. Epochs were randomized, so order does not reflect recording sequence. 

## Background

In human memory research, we typically train decoders on the visual peak of a localizer and then apply them to, e.g., resting-state data, expecting a learned sequence to be decodable. However, it is questionable to what extent the replayed representations correspond to the visual peak patterns the decoder extracted. Evidence suggests that memory representations—or even sensory stimulation from different modalities—have limited overlap with visually evoked stimulus processing patterns ([Bezsudnova et al., 2024](https://direct.mit.edu/jocn/article/36/8/1760/121050); [Dijkstra et al., 2019](https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(19)30059-2); [Dijkstra et al., 2021](https://www.eneuro.org/content/8/5/ENEURO.0228-21.2021.abstract)). Failure to transcode from visual presentation to imagined visual stimuli would challenge the current interpretation of decoders in many memory-processing studies.

## Getting Started

1. To get started, download the data from https://doi.org/10.5281/zenodo.17351690.
2. Have a look at the example [notebook](https://github.com/skjerns/imagine-decoding-challenge/tree/main/examples)
3. Tinker around and find a way to predict the mental imagery
4. Submit your improved solution via Kaggle to this competition: https://www.kaggle.com/competitions/the-imagine-decoding-challenge


## Things to keep in mind:

- Your task is to train a classifier on the data after stimulus onset of the localizer. While it's probably possible to look at the labels of imagine trials in the train-set and try cross-decoding across participants without the localizer data, this is not the goal
- The `imagine` trials were recorded after participants learned some image associations (i.e., image sequences). Subconscious reactivation of associated stimuli after the word cue is possible, though we expect the instructed imagery pattern to **supersede** these reactivation effects in decoding strength.
