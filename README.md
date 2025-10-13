# imagine-decoding-challenge

The epochs have been scrambled! Can you figure out in which epoch we played which auditory stimulus by training a visual decoder?

## Overview

Can you decode which images people were thinking of by data of visually seeing these images?

In memory research, decoders are often trained on localizer data to extract neural activation patterns of specific stimuli (e.g. "what pattern occurs when we see a clown"). Then, taken as evidence for reprocessing, these decoders are used to detect presence of these patterns in other parts of the experiment (e.g. "after learning something about clowns, we can see the activation pattern of 'clown' being more active than expected"). However, how well does this actually work?

We've recorded a **localizer** in the [MEG](https://en.wikipedia.org/wiki/Magnetoencephalography) with 30 participants in which we presented one of **ten visual stimuli** in random order (see `Localizer` section). Then they performed the study reported in Kern et al. ([2024](https://elifesciences.org/articles/93357) & [2025](https://elifesciences.org/reviewed-preprints/108023)). Right after the end of our experiment we asked them to close their eyes and once again **played the words** that describe the stimuli. Additionally we tasked them to **imagine the cued image** as vividly as possible whenever they hear its word (see `Imagine` section).

Unfortunately, last night a **mean** **gnome** came to our data centre and **scrambled** the order of the `imagine` trials! Can you help us re-assign the stimulus labels to the epochs of the `imagine` trials?

**Goal:** The epochs have been scrambled! Can you figure out in which epoch we played which word as a auditory stimulus by training decoder on visual images of the words?

#### Idea

In human replay research, we traditionally train a decoders on the visual peak of a localizer and then apply this decoder to e.g. a resting state, expecting the a learned sequence to be decodable. However, it is questionable to what extend the replayed representations will correspond to the pattern that the decoder extracted from the visual peak. There's evidence that memory representations or even sensory stimulation from different modalities have rather small overlap to visual evoked stimulus processing patterns ([Bezsudnova et al., 2024](https://direct.mit.edu/jocn/article/36/8/1760/121050); [Dijkstra et al., 2019](https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(19)30059-2), [Dijkstra et al. 2021](https://www.eneuro.org/content/8/5/ENEURO.0228-21.2021.abstract)).

## Localizer trials

## Imagine trials
