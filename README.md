# imagine-decoding-challenge

The epochs have been scrambled! Can you figure out in which epoch we played which auditory word by training a visual decoder of images of the words?

## Overview

Can you decode which images people were thinking of by data of visually seeing these images?

In memory research, decoders are often trained on localizer data to extract neural activation patterns of specific stimuli (e.g. "what pattern occurs when we see a clown"). Taken as evidence for reprocessing, these decoders are then used to detect pattern presences in other parts of the experiment (e.g. "after learning something about clowns, we can see the activation pattern of 'clown' being more active than expected, that means, knowledge is being consolidated!"). However, how well does this actually work? 

We've recorded a simple paradigm in the [Magnetoencephalograph (MEG)](https://en.wikipedia.org/wiki/Magnetoencephalograph) in which we showed [ten different visual items](https://github.com/skjerns/imagine-decoding-challenge/blob/main/md_assets/stimuli.png) many times to participants. Later, we played back spoken words describing the items while they had their eyes closed, and we asked them to mentally visualize the items associated to the word as vividly as possible. Can you train a decoder on the visual presentation ("localizer") and decode which item people mentalized?

## Experiment

We've recorded a **localizer** in the [MEG](https://en.wikipedia.org/wiki/Magnetoencephalography) with 30 participants in which we presented one of [ten different items](https://github.com/skjerns/imagine-decoding-challenge/blob/main/md_assets/stimuli.png) in random order. In each trial, they first heard a word describing the item (e.g. "clown") for ~1 second, then they saw a visual image that either matched (i.e. was "clown") or not, in which case they had to press a button. After that, they performed the study reported in Kern et al. ([2024](https://elifesciences.org/articles/93357) & [2025](https://elifesciences.org/reviewed-preprints/108023)). Right after the end of the main experiment we asked them to close their eyes and once again **played the words** that describe the stimuli. We tasked them to **imagine the cued image** as vividly as possible whenever they hear its word.

**Goal:** The epochs have been scrambled! Can you figure out in which epoch we played which word as a auditory stimulus by training decoder on visual images of the words?

<u>Example of the localizer:</u>

https://github.com/skjerns/imagine-decoding-challenge/raw/refs/heads/main/md_assets/presentation_localizer.mp4

Instructions: *"Press a button if there is a mismatch between word and image"*

<u>Example of the imagine trials:</u>

https://github.com/skjerns/imagine-decoding-challenge/raw/refs/heads/main/md_assets/presentation_imagine.mp4

Instructions: *"Close your eyes and mentally imagine the image belonging to the word you hear as vividly as possible"*



## The Data

The data consists of `mne.Epochs` of the `localizer` and the `imagine` trials. The data have been preprocessed with [tSSS MaxFilter](https://imaging.mrc-cbu.cam.ac.uk/meg/Maxfilter) and resampled to 100 Hz. Continuous HPI has been recorded and used to re-align the head position to the mean position in the localizer. No alignment between participants was performed, so sensor positions might record slightly different parts of participant's brains. The epochs are aligned with the visual stimulus onset (`localizer`) or the word onset (`imagine`). The `localizer` epochs have intentionally been truncated and baseline corrected to remove the signal of the word processing before the visual onset. Besides that, no preprocessing has been applied, and depending on who you ask is probably [not necessary](https://www.nature.com/articles/s41598-023-27528-0) or [might be useful](https://www.nature.com/articles/s42003-025-08464-3).  We recorded 306 MEG channels a MEGIN Triux, of which 102 are magnetometers and 204 are planar gradiometers ([vectorview layout](https://mne.tools/stable/generated/mne.channels.Layout.html#mne-channels-layout)). Additionally, we recorded ECG and horizontal and vertical EOG.

**Localizer**: There are 480 `localizer` epochs, 48 for each stimulus item. Each trial is cropped from -200ms before visual onset until 1000ms after onset. The trials in which there was a mismatch between word and image have already been removed. Baseline correction was applied using the data before visual onset. Each trial has a label belonging to one of the stimuli.

**Imagine**: The `imagine` epochs have been cropped from -200ms to 5000ms after word onset, with no baseline correction. There are either 35 or 50 epochs per participant, with either 3-4 or 5 trials per stimulus. Trial labels have been removed from these epochs, and each trial has been given a number instead. Epochs have been randomized, so they are not in the order that they have been recorded. Important caveat, the `imagine` trials have been recorded after participants learned associations of the images (i.e. a sequence of images). It is possible that there is subconscious reactivation after the word cue of associated stimuli. However, we suspect that the instructed imagery pattern should superseed these reactivation patterns in decoding strength.

## Background

In human memory research, we traditionally train a decoders on the visual peak of a localizer and then apply this decoder to e.g. a resting state, expecting the a learned sequence to be decodable. However, it is questionable to what extend the replayed representations will correspond to the pattern that the decoder extracted from the visual peak. There's evidence that memory representations or even sensory stimulation from different modalities have rather small overlap to visual evoked stimulus processing patterns ([Bezsudnova et al., 2024](https://direct.mit.edu/jocn/article/36/8/1760/121050); [Dijkstra et al., 2019](https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(19)30059-2), [Dijkstra et al. 2021](https://www.eneuro.org/content/8/5/ENEURO.0228-21.2021.abstract)). However, if we cannot transcode from visual presentation to imagined visual stimuli, this would weaken the case for the current usage of decoders in many memory  processing studies.

## Getting started

To get started, download the data from XXX.

We supply a script with a standard pipeline that can decode the `localizer` trials in a cross-validation using a logistic regression. To verify your solution, we have setup a Kaggle competition. You can upload your solutions there and check how well your decoder was able to differentiate the `imagine` trials.
