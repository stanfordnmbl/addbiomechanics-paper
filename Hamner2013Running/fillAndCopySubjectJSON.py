import json
import pandas as pd
import os


def fillAndCopySubjectJSON():

    # Load subject demographics.
    demographics_df = pd.read_csv('demographics.csv')
    subjects = demographics_df['subject']
    masses = demographics_df['weight (kg)']
    heights = demographics_df['height (m)']

    # Fill out the template '_subject.json' and copy it to the subject directory
    # under 'Formatted'.
    for subject, mass, height in zip(subjects, masses, heights):
        if not os.path.isdir(os.path.join('Formatted', subject)):
            os.mkdir(os.path.join('Formatted', subject))

        # Load template.
        f = open(os.path.join('_subject.json'))
        data = json.load(f)

        # We only set the mass and height here, but other flags passed to engine.py
        # could be set here (e.g., 'tuneResidualLoss' and 'maxTrialsToSolveMassOver').
        data['massKg'] = mass
        data['heightM'] = height
        data['disableDynamics'] = False
        data['segmentTrials'] = False
        data['useReactionWheels'] = True

        # Write out filled template file to the 'Formatted' directory.
        dest_fpath = os.path.join('Formatted', subject, '_subject.json')
        with open(dest_fpath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fillAndCopySubjectJSON()
