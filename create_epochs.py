#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 09:51:27 2025

obfuscated version of the script used to create the epochs for the challenge

@author: simon.kern
"""
from pathlib import Path
import mne
import settings
import time
import utils
import numpy as np
from tqdm import tqdm
import pandas as pd
from joblib import Memory

mem = Memory('/data/joblib-imagine/')
stim_translation = {
    'apfel': 'apple',
    'berg': 'mountain',
    'clown': 'clown',
    'fahrrad': 'bicycle',
    'fuß': 'foot',
    'kuchen': 'cake',
    'pinsel': 'brush',
    'schreibtisch': 'desk',
    'tasse': 'cup',
    'zebra': 'zebra'
}

@mem.cache
def load_resample(filenames, sfreq=100):
    if isinstance(filenames, str):
        filenames = [filenames]
    raws = [mne.io.read_raw(x, preload=True) for x in filenames]
    raw = mne.concatenate_raws(raws)
    events = mne.find_events(raw, min_duration=3/1000)
    raw, events = raw.resample(sfreq, events=events, n_jobs=-1)
    return raw, events

mne.set_log_level('WARNING')  # options: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'

outpath = Path(settings.data_dir) / 'imagine_challenge'
data_path = Path(settings.data_dir) / 'seq12'

outpath.mkdir(exist_ok=True)

paths = sorted([x for x in list(data_path.iterdir()) if 'DSMR' in str(x)])
subjects = [x.name for x in paths]

df_test = pd.DataFrame()
df_train = pd.DataFrame()

for j, (subj, path) in enumerate(zip(tqdm(subjects), paths)):

    i = int(subj[-2:])
    # check if files are present
    files_localizer = list(sorted(path.rglob('localizer*fif')))
    assert len(files_localizer) == 2

    files_imagine = list(sorted(path.rglob('imag*fif')))
    if len(files_imagine) != 1:
        print(f'NO IMAGINE FILE FOR {subj=}')
        continue
    subj_id = f'sub-{i:02d}'

    #### OBFUSCATED LINE
    #### OBFUSCATED LINE

    curr_set = 'train' if j%2 else 'test'

    subj_dir = outpath / curr_set / subj_id
    subj_dir.mkdir(exist_ok=True, parents=True)

    # first load localizers
    raw, events = load_resample(files_localizer)

    # create epochs for each image presentation
    event_id = {stim_translation[name]:i+1 for i, name in enumerate(utils.get_image_names(subj))}
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.2, tmax=1, preload=True)
    epochs.pick(['meg', 'bio'])
    epochs.set_channel_types({'BIO001': 'ecg', 'BIO002': 'eog', 'BIO003': 'eog'})
    epochs.rename_channels({'BIO001': 'ECG', 'BIO002': 'HEOG', 'BIO003': 'VEOG'})

    # reorder event ids to stimulus names alphabetically
    event_id_sorted = {name: i+1 for i, name in enumerate(sorted(event_id))}
    epochs.events[:, 2] += 100  # offset by 100 before reassigning
    for (name, idx) in event_id_sorted.items():
        # check which idx this stimulus had before
        orig_idx = event_id[name]
        # remap to new idx that is alphabetically sorted
        epochs.events[epochs.events[:, 2]==orig_idx+100, 2] = idx

    # assign new alphabetical list to participant
    epochs.event_id = event_id_sorted
    epochs.save(subj_dir /  f'{subj_id}_localizer-epo.fif', overwrite=True)

    # for good measure, save the real labels in a csv
    mapping = {val: key for key, val in epochs.event_id.items()}
    y_true = [mapping[idx] for idx in epochs.events[:, 2]]
    df_events_localizer = pd.DataFrame({'subject': subj_id,
                                        'trial_idx': np.arange(1, len(epochs)+1),
                                        'label': y_true,
                                        'trigger': epochs.events[:, 2],
                                        'trial_type': 'localizer'
                                       })
    df_events_localizer.to_csv(subj_dir / f'{subj_id}_localizer-labels.csv',
                               index=False)

    # next load the imagine files
    raw, events = load_resample(files_imagine)

    # get trigger mapping to image names
    event_id = {stim_translation[name]:i+1 for i, name in enumerate(utils.get_image_names(subj))}

    # create epochs for each auditory cue presentation
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.2, tmax=5, preload=True)
    epochs.pick(['meg', 'bio'])
    epochs.set_channel_types({'BIO001': 'ecg', 'BIO002': 'eog', 'BIO003': 'eog'})
    epochs.rename_channels({'BIO001': 'ECG', 'BIO002': 'HEOG', 'BIO003': 'VEOG'})

    # reorder event ids to stimulus names alphabetically
    event_id_sorted = {name: i+1 for i, name in enumerate(sorted(event_id))}
    epochs.events[:, 2] += 100  # offset by 100 before reassigning
    for (name, idx) in event_id_sorted.items():
        # check which idx this stimulus had before
        orig_idx = event_id[name]
        # remap to new idx that is alphabetically sorted
        epochs.events[epochs.events[:, 2]==orig_idx+100, 2] = idx
    epochs.event_id = event_id_sorted

    # shuffle epochs for good measure
    #### OBFUSCATED LINE
    #### OBFUSCATED LINE
    epochs = epochs[idx_shuf]

    # obfuscate event onsets
    epochs.events[:, 0] = np.arange(len(epochs.events))*200+100

    # save true labels for later
    mapping = {val: key for key, val in epochs.event_id.items()}
    y_true = [mapping[idx] for idx in epochs.events[:, 2]]
    df_events = pd.DataFrame({'subject': subj_id,
                              'trial_idx': np.arange(1, len(epochs)+1),
                              'label': y_true,
                              'trigger': epochs.events[:, 2],
                              'trial_type': 'imagine'
                               })

    # remove all labels if we are in the test set
    if curr_set=='train':
        df_train = pd.concat([df_train, df_events], ignore_index=True)

        # save event csv for the train set
        df_events.to_csv(subj_dir / f'{subj_id}_imagine-labels.csv',
                               index=False)

    elif curr_set=='test':
        df_test = pd.concat([df_test, df_events], ignore_index=True)

        # remove labels
        epochs.events[:, 2] = np.arange(len(epochs))+1
        epochs.event_id = {f'unknown/{i+1}': i+1 for i in range(len(epochs))}

    else:
        raise Exception('sanity check failed')

    epochs.save(subj_dir /  f'{subj_id}_imagine-epo.fif', overwrite=True)

# actual labels
df_train.to_csv(outpath / 'train' / 'labels_imagine-train.csv', index=False)

# also save ground truth, but don't publish
df_test.to_csv(outpath / 'labels_imagine-test.csv', index=False)

# create ground truth solution labels
df_solution = pd.DataFrame()
df_solution['ID'] = df_test['subject'] + '_' + df_test['trial_idx'].astype(str)
df_solution['label'] = df_test['label']
df_solution['Usage'] = 'Public'
df_solution.to_csv(outpath / 'prediction-solution.csv', index=False)

# fill example submission with random data
np.random.seed(int(time.time()))
df_example = df_solution[['ID', 'label']]
df_example.loc[:, 'label'] = np.random.choice(list(event_id), len(df_example))
df_example.to_csv(outpath / 'prediction-example.csv', index=False)
