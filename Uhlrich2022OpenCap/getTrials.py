import os
import json


def getTrials(subject):
    f = open(os.path.join('excluded_trials.json'))
    data = json.load(f)
    markers_fpath = os.path.join('Raw', subject, 'MarkerData', 'Mocap')
    marker_files = os.listdir(markers_fpath)
    trials = list()
    for trial in [trial.replace('.trc', '') for trial in marker_files if trial.endswith('.trc')]:
        excludeTrial = False
        for excluded_trial in data['excluded_trials']:
            if excluded_trial in trial:
                excludeTrial = True
        if not excludeTrial:
            trials.append(trial)
    f.close()

    f = open(os.path.join('excluded_trials_subjects.json'))
    data_subjects = json.load(f)
    trials_to_remove = list()
    if subject in data_subjects:
        for excluded_trial in data_subjects[subject]:
            trials_to_remove.append(excluded_trial)
    f.close()

    for trial in trials_to_remove:
        if trial in trials:
            trials.remove(trial)

    return trials