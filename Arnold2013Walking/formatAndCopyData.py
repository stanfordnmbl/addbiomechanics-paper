import os
import opensim as osim
import shutil
import pandas as pd
from helpers import create_markers_table, create_external_loads_table_for_gait, \
                    create_model_processor, create_static_trial_markers, \
                    create_coordinates_from_solution

regression_fpath = os.path.join('regression')
formatted_fpath = os.path.join('Formatted')
if not os.path.isdir(formatted_fpath):
    os.mkdir(formatted_fpath)

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']

includeStatic = False
lockToes = True
for subject in subjects:

    # Create regression folders.
    subject_fpath = os.path.join(regression_fpath, subject)
    if not os.path.isdir(subject_fpath):
        os.mkdir(subject_fpath)

    trials_fpath = os.path.join(subject_fpath, 'trials')
    if not os.path.isdir(trials_fpath):
        os.mkdir(trials_fpath)

    trial_fpath = os.path.join(trials_fpath, 'walk2')
    if not os.path.isdir(trial_fpath):
        os.mkdir(trial_fpath)

    # Create Formatted folders.
    subject_fpath = os.path.join('Formatted', subject)
    if not os.path.isdir(subject_fpath):
        os.mkdir(subject_fpath)

    trials_fpath = os.path.join(subject_fpath, 'trials')
    if not os.path.isdir(trials_fpath):
        os.mkdir(trials_fpath)

    trial_fpath = os.path.join(trials_fpath, 'walk2')
    if not os.path.isdir(trial_fpath):
        os.mkdir(trial_fpath)

    # Model file.
    model_src = os.path.join('Raw', 'unscaled_generic_registered.osim')
    model_dst = os.path.join('Formatted', subject, 'unscaled_generic.osim')
    shutil.copyfile(model_src, model_dst)

    # Load scaled model to compute synthetic data.
    model_fpath = os.path.join('Raw', subject, f'{subject}_final_reregistered.osim')
    modelProcessor = create_model_processor(model_fpath, weld_wrist=True)
    model = modelProcessor.process()

    # Create static trial data.
    if includeStatic:
        if not os.path.isdir(os.path.join('Formatted', subject, 'trials', 'static')):
            os.mkdir(os.path.join('Formatted', subject, 'trials', 'static'))
        # Create static trial markers file.
        static_markers = create_static_trial_markers(model)
        static_trc_fpath = os.path.join('Formatted', subject, 'trials', 'static', 'markers.trc')
        trc = osim.TRCFileAdapter()
        trc.write(static_markers, static_trc_fpath)

    # Create ground reaction forces file.
    unperturbed_fpath = os.path.join('Raw', subject, 'unperturbed.sto')
    table = create_external_loads_table_for_gait(model, unperturbed_fpath)
    sto = osim.STOFileAdapter()
    grf_fpath = os.path.join('Formatted', subject, 'trials', 'walk2', 'grf.mot')
    sto.write(table, grf_fpath)
    reg_grf_fpath = os.path.join('regression', subject, 'trials', 'walk2', 'grf.mot')
    sto.write(table, reg_grf_fpath)

    # Create synthetic markers file.
    solution = osim.MocoTrajectory(unperturbed_fpath)
    modelProcessor = create_model_processor(model_fpath, weld_toes=lockToes, weld_wrist=True)
    model = modelProcessor.process()
    model.printToXML(os.path.join('regression', subject, f'{subject}.osim'))
    statesTable = solution.exportToStatesTable()
    statesTrajectory = osim.StatesTrajectory.createFromStatesTable(model, statesTable, False, True, False)
    markers = create_markers_table(model, statesTrajectory)
    trc_fpath = os.path.join('Formatted', subject, 'trials', 'walk2', 'markers.trc')
    trc = osim.TRCFileAdapter()
    trc.write(markers, trc_fpath)
    reg_trc_fpath = os.path.join('regression', subject, 'trials', 'walk2', 'markers.trc')
    trc.write(markers, reg_trc_fpath)

    # Create coordinates file.
    coordinates = create_coordinates_from_solution(unperturbed_fpath)
    coordinates_fpath = os.path.join('regression', subject, 'coordinates.sto')
    sto.write(coordinates, coordinates_fpath)

    # Create directories under Processed.
    if not os.path.isdir(os.path.join('Processed', subject)):
        os.mkdir(os.path.join('Processed', subject))
