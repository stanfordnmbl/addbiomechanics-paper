import pandas as pd
import os
import shutil
from getTrials import getTrials

# Folder locations. We will reformat and trim the data located
# in the 'Raw' folder and copy it to the 'Formatted' folder.
raw_fpath = os.path.join('Raw')
formatted_fpath = os.path.join('Formatted')

# Load subject demographics.
demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
weights = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
sexes = demographics_df['sex']

# Process and copy the data!
print('Copying data for AddBiomechanics processing...')
for subject, weight, height, sex in zip(subjects, weights, heights, sexes):
    subject_path = os.path.join(formatted_fpath, subject)
    if not os.path.isdir(subject_path):
        os.mkdir(subject_path)

    trials_path = os.path.join(subject_path, 'trials')
    if not os.path.isdir(trials_path): os.mkdir(trials_path)

    # Copy the generic musculoskeletal model.
    model_src = os.path.join('Raw', 'LaiArnoldModified2017_poly_withArms_weldHand_generic.osim')
    model_dst = os.path.join(formatted_fpath, subject, 'unscaled_generic.osim')
    shutil.copyfile(model_src, model_dst)

    # Get trial names for this subject.
    trials = getTrials(subject)

    # Loop through the trials for this subject.
    for trial in trials:
        print(f'--> {subject}, {trial}')

        trial_path = os.path.join(trials_path, trial)
        if not os.path.isdir(trial_path): os.mkdir(trial_path)

        # Copy the ground reaction forces.
        grf_src = os.path.join(raw_fpath, subject, 'ForceData', f'{trial}_forces.mot')
        grf_dst = os.path.join(trial_path, 'grf.mot')
        shutil.copyfile(grf_src, grf_dst)

        # Copy the marker trajectories.
        marker_src = os.path.join(raw_fpath, subject, 'MarkerData', 'Mocap', f'{trial}.trc')
        marker_dst = os.path.join(trial_path, 'markers.trc')
        shutil.copyfile(marker_src, marker_dst)
