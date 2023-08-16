import pandas as pd
import os
import opensim as osim
import json
import numpy as np
import shutil


def fill_analysis_template(template, setup, trial, model, results,
                           startTime, endTime, extLoads, coordinates):
    ft = open(template)
    content = ft.read()
    content = content.replace('@TRIAL@', trial)
    content = content.replace('@MODEL@', model)
    content = content.replace('@RESULTS_DIR@', results)
    content = content.replace('@START_TIME@', f'{startTime:.4f}')
    content = content.replace('@END_TIME@', f'{endTime:.4f}')
    content = content.replace('@EXT_LOADS@', extLoads)
    content = content.replace('@COORDINATES@', coordinates)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


def fill_extloads_template(template, setup, subject, trial, grf_file):
    ft = open(template)
    content = ft.read()
    content = content.replace('@SUBJECT@', subject)
    content = content.replace('@TRIAL@', trial)
    content = content.replace('@GRF_FILE@', grf_file)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()

# Create results folder.
if not os.path.isdir(os.path.join('residuals', 'opencap')):
    os.mkdir(os.path.join('residuals', 'opencap'))
opencap_fpath = os.path.join('residuals', 'opencap', 'results')
if not os.path.isdir(opencap_fpath):
    os.mkdir(opencap_fpath)

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']

marker_rmse = np.zeros((len(subjects)))
marker_max = np.zeros((len(subjects)))
for isubj, (subject, mass, height) in enumerate(zip(subjects, masses, heights)):

    # Create subject folder.
    subject_fpath = os.path.join(opencap_fpath, subject)
    if not os.path.isdir(subject_fpath):
        os.mkdir(subject_fpath)

    # Model path
    model_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'Model',
                               'LaiArnoldModified2017_poly_withArms_weldHand_scaled.osim')

    # Get trial names for this subject.
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

    # Loop over all trials for this subject
    marker_rmse_trials = np.zeros((len(trials)))
    marker_max_trials = np.zeros((len(trials)))
    for itrial, trial in enumerate(trials):

        # Create Analysis folder
        trial_fpath = os.path.join(subject_fpath, trial)
        if not os.path.isdir(trial_fpath):
            os.mkdir(trial_fpath)
        analysis_fpath = os.path.join(trial_fpath, 'Analysis')
        if not os.path.isdir(analysis_fpath):
            os.mkdir(analysis_fpath)

        # File paths
        coordinates_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'IK', f'{trial}.mot')
        grf_fpath = os.path.join('Raw', subject, 'ForceData', f'{trial}_forces.mot')
        id_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'ID', f'{trial}.sto')

        # Get initial and final time
        coordinates = osim.TimeSeriesTable(coordinates_fpath)
        initial_time = coordinates.getIndependentColumn()[0]
        final_time = coordinates.getIndependentColumn()[-1]

        # Fill external loads template
        template_fpath = os.path.join('templates', 'external_loads_opencap.xml')
        extloads_fpath = os.path.join(analysis_fpath, f'{trial}_external_loads.xml')
        fill_extloads_template(template_fpath, extloads_fpath, subject, trial,
                               os.path.relpath(grf_fpath, analysis_fpath))

        # Fill and write Analysis setup file template
        template_fpath = os.path.join('templates', 'setup_analysis.xml')
        setup_fpath = os.path.join(analysis_fpath, f'{subject}_{trial}_setupAnalysis.xml')

        results_fpath = os.path.join(analysis_fpath, f'results_{trial}')
        fill_analysis_template(
            template_fpath, setup_fpath, trial,
            os.path.relpath(model_fpath, analysis_fpath),
            os.path.relpath(results_fpath, analysis_fpath),
            initial_time, final_time,
            os.path.relpath(extloads_fpath, analysis_fpath),
            os.path.relpath(coordinates_fpath, analysis_fpath))

        # Run Analysis to compute center of mass trajectories
        analyze = osim.AnalyzeTool(setup_fpath)
        analyze.run()

        # Load center of mass results
        com = osim.TimeSeriesTable(os.path.join(results_fpath,
                                                f'analysis_{trial}_BodyKinematics_pos_global.sto'))

        # Write all files
        sto = osim.STOFileAdapter()
        shutil.copyfile(grf_fpath, os.path.join('residuals', 'opencap', f'{subject}_{trial}_grf.mot'))
        shutil.copyfile(id_fpath, os.path.join('residuals', 'opencap', f'{subject}_{trial}_residuals.sto'))
        sto.write(com, os.path.join('residuals', 'opencap', f'{subject}_{trial}_com.sto'))

        # Compute marker RMSE
        marker_errors_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'IK',
                                           f'{trial}_ik_marker_errors.sto')
        marker_errors = osim.TimeSeriesTable(marker_errors_fpath)
        marker_rmse_trials[itrial] = np.mean(marker_errors.getDependentColumn('marker_error_RMS').to_numpy())
        marker_max_trials[itrial] = np.max(marker_errors.getDependentColumn('marker_error_RMS').to_numpy())

    marker_rmse[isubj] = np.mean(marker_rmse_trials)
    marker_max[isubj] = np.max(marker_max_trials)

# Save marker_rmse_subject to a CSV file
with open('marker_rmse_opencap.csv', 'w') as f:
    f.write('Subject,Marker RMSE (m)\n')
    for subject, rmse in zip(subjects, marker_rmse):
        f.write(f'{subject},{rmse}\n')

# Save marker_max_subject to a CSV file
with open('marker_max_opencap.csv', 'w') as f:
    f.write('Subject,Marker Max Error (m)\n')
    for subject, maxError in zip(subjects, marker_max):
        f.write(f'{subject},{maxError}\n')