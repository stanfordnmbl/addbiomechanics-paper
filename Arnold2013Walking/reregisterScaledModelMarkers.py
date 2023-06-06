import os
import opensim as osim
import shutil
import pandas as pd
from helpers import apply_generic_marker_offsets_to_model

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']

regression_fpath = os.path.join('regression')
if not os.path.isdir(regression_fpath):
    os.mkdir(regression_fpath)

# Move generic model to regression folder.
model_src = os.path.join('Raw', 'unscaled_generic_registered.osim')
model_dst = os.path.join(regression_fpath, 'unscaled_generic.osim')
shutil.copyfile(model_src, model_dst)

includeStatic = False
lockToes = True
for subject in subjects:

    # Model file.
    model_src = os.path.join('Raw', 'unscaled_generic_registered.osim')
    model_dst = os.path.join('Raw', subject, f'{subject}_final_reregistered.osim')
    scaled_model_fpath = os.path.join('Raw', subject, f'{subject}_final.osim')
    scaled = apply_generic_marker_offsets_to_model(model_src, scaled_model_fpath, model_dst)

