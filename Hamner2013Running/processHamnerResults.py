import pandas as pd
import os
import opensim as osim
import json
import xml.etree.ElementTree as ET
import numpy as np
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict


def fill_analysis_template(template, setup, trial, cycle, model, results,
                           startTime, endTime, extLoads, coordinates):
    ft = open(template)
    content = ft.read()
    content = content.replace('@TRIAL@', f'{trial}_cycle{cycle}')
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


def fill_extloads_template(template, setup, trial, grf_file):
    ft = open(template)
    content = ft.read()
    content = content.replace('@TRIAL@', trial)
    content = content.replace('@GRF_FILE@', grf_file)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


def get_rra_timerange(subject, cycle, ik_tag):
    rra_setup = os.path.join('Raw', subject, 'rra_multipleSteps',
                             f'RRA_Results_v191_{ik_tag}',
                             f'{subject}_Setup_RRA_{ik_tag}_cycle{cycle}_v191.xml')
    rra_setup_no_header = os.path.join('Raw', subject, 'rra_multipleSteps',
                                       f'RRA_Results_v191_{ik_tag}',
                                       f'{subject}_Setup_RRA_{ik_tag}_cycle{cycle}_v191_no_header.xml')
    with open(rra_setup) as f:
        with open(rra_setup_no_header, 'w') as f2:
            endheader = 0
            lines = f.readlines()
            for line in lines:
                if line.startswith('<?xml version'):
                    break
                endheader += 1

            f2.writelines(lines[endheader:])

    tree = ET.parse(rra_setup_no_header)
    root = tree.getroot()
    itime = float(root[0].find('initial_time').text)
    ftime = float(root[0].find('final_time').text)

    return itime, ftime


def create_markers_table(model_fpath, coordinates_fpath):

    includedMarkers = list()
    includedMarkers.append('CLAV')
    # includedMarkers.append('C7')
    for side in ['R', 'L']:
        includedMarkers.append(f'{side}ASI')
        includedMarkers.append(f'{side}PSI')
        includedMarkers.append(f'{side}TH1')
        # includedMarkers.append(f'{side}TH2')
        includedMarkers.append(f'{side}TH3')
        includedMarkers.append(f'{side}TB1')
        includedMarkers.append(f'{side}TB2')
        includedMarkers.append(f'{side}TB3')
        includedMarkers.append(f'{side}CAL')
        includedMarkers.append(f'{side}MT5')
        includedMarkers.append(f'{side}TOE')
        includedMarkers.append(f'{side}ACR')
        includedMarkers.append(f'{side}UA1')
        includedMarkers.append(f'{side}UA2')
        includedMarkers.append(f'{side}UA3')
        includedMarkers.append(f'{side}LEL')
        includedMarkers.append(f'{side}MEL')
        includedMarkers.append(f'{side}FAsuperior')
        includedMarkers.append(f'{side}FAradius')
        includedMarkers.append(f'{side}FAulna')

    modelProcessor = osim.ModelProcessor(model_fpath)
    jointsToWeld = ['subtalar_r', 'subtalar_l', 'mtp_r', 'mtp_l', 'radius_hand_r', 'radius_hand_l']
    modelProcessor.append(osim.ModOpReplaceJointsWithWelds(jointsToWeld))
    model = modelProcessor.process()
    model.initSystem()
    markersTable = osim.TimeSeriesTableVec3()
    coordinatesDegrees = osim.TimeSeriesTable(coordinates_fpath)
    coordinatesDegrees.addTableMetaDataString('inDegrees', 'yes')
    tableProcessor = osim.TableProcessor(coordinatesDegrees)
    tableProcessor.append(osim.TabOpConvertDegreesToRadians())
    coordinates = tableProcessor.process(model)

    statesTrajectory = osim.StatesTrajectory.createFromStatesTable(model, coordinates, True, True, False)
    numStates = statesTrajectory.getSize()

    markerSet = model.getMarkerSet()
    numMarkers = markerSet.getSize()
    for istate in range(numStates):
        state = statesTrajectory.get(istate)
        model.realizePosition(state)
        row = osim.RowVectorVec3(len(includedMarkers))
        for imarker, marker_name in enumerate(includedMarkers):
            marker = markerSet.get(marker_name)
            row[imarker] = marker.getLocationInGround(state)

        markersTable.appendRow(state.getTime(), row)

    # Create table.
    labels = osim.StdVectorString()
    for marker_name in includedMarkers:
        labels.append(marker_name)

    markersTable.setColumnLabels(labels)

    time = np.array(markersTable.getIndependentColumn())
    dt = time[1] - time[0]
    datarate = 1 / dt
    markersTable.addTableMetaDataString('DataRate', str(datarate))
    markersTable.addTableMetaDataString('Units', 'm')

    return markersTable


if not os.path.isdir(os.path.join('residuals', 'hamner')):
    os.mkdir(os.path.join('residuals', 'hamner'))

hamner_fpath = os.path.join('residuals', 'hamner', 'results')
if not os.path.isdir(hamner_fpath):
    os.mkdir(hamner_fpath)

demographics_df = pd.read_csv('demographics.csv')

subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
trials = ['run200', 'run300', 'run400', 'run500']
marker_rmse = np.zeros((len(subjects), len(trials)))
marker_rmse_subject = np.zeros((len(subjects)))
for isubj, (subject, mass, height) in enumerate(zip(subjects, masses, heights)):
    # Model path
    model_fpath = os.path.join(hamner_fpath, subject, 'model.osim')

    # Loop over all trials for this subject
    for itrial, trial in enumerate(trials):

        # Create Analysis folder
        analysis_fpath = os.path.join(hamner_fpath, subject, 'trials', trial, 'Analysis')
        if not os.path.isdir(analysis_fpath):
            os.mkdir(analysis_fpath)

        # update data tags, if needed
        tag = '02'
        if subject in subject_dict.keys():
            for tag_tuple in subject_dict[subject]:
                if tag_tuple[0] == trial:
                    tag = tag_tuple[1]

        data_tag = f'{trial_dict[trial]} {tag}'
        ik_tag = f'{trial_dict[trial]}{tag}'

        cycle_dicts = [init_cycle_dict, second_cycle_dict, final_cycle_dict]
        cycles = [1, 2, 3]
        marker_rmse_cycles = list()
        for cycle, cycle_dict in zip(cycles, cycle_dicts):
            # update cycle number, if needed
            if subject in cycle_dict.keys():
                for cycle_tuple in cycle_dict[subject]:
                    if cycle_tuple[0] == trial:
                        cycle = cycle_tuple[1]

            initial_time, final_time = get_rra_timerange(subject, cycle, ik_tag)

            # File paths
            coordinates_fpath = os.path.join(hamner_fpath, subject, 'trials', trial,
                                             f'{subject}_{trial}_cycle{cycle}_coordinates.sto')
            grf_fpath = os.path.join('residuals', 'hamner', f'{subject}_{trial}_cycle{cycle}_grf.mot')

            # Fill external loads template
            template_fpath = os.path.join('external_forces_hamner.xml')
            extloads_fpath = os.path.join(analysis_fpath, f'{trial}_external_forces.xml')
            fill_extloads_template(template_fpath, extloads_fpath, trial,
                                   os.path.relpath(grf_fpath, analysis_fpath))

            # Fill and write Analysis setup file template
            template_fpath = os.path.join('setup_analysis.xml')
            setup_fpath = os.path.join(analysis_fpath, f'{subject}_{trial}_cycle{cycle}_setupAnalysis.xml')

            model_fpath = os.path.join(hamner_fpath, subject, 'model.osim')
            results_fpath = os.path.join(analysis_fpath, f'results_{trial}_cycle{cycle}')
            fill_analysis_template(
                template_fpath, setup_fpath, trial, cycle,
                os.path.relpath(model_fpath, analysis_fpath),
                os.path.relpath(results_fpath, analysis_fpath),
                initial_time, final_time,
                os.path.relpath(extloads_fpath, analysis_fpath),
                os.path.relpath(coordinates_fpath, analysis_fpath))

            # Run Analysis to compute center of mass trajectories
            analyze = osim.AnalyzeTool(setup_fpath)
            analyze.run()

            # Load files
            com = osim.TimeSeriesTable(os.path.join(results_fpath,
                                                    f'analysis_{trial}_cycle{cycle}_BodyKinematics_pos_global.sto'))
            # Write all files
            sto = osim.STOFileAdapter()
            sto.write(com, os.path.join('residuals', 'hamner', f'{subject}_{trial}_cycle{cycle}_com.sto'))

            # Compute marker errors
            rra_markers = create_markers_table(model_fpath, coordinates_fpath)
            # trc = osim.TRCFileAdapter()
            # trc.write(rra_markers, os.path.join('Formatted', subject, 'trials', trial, 'markers_rra.trc'))
            trc_markers = osim.TimeSeriesTableVec3(os.path.join('Formatted', subject, 'trials', trial, 'markers.trc'))
            marker_names = trc_markers.getColumnLabels()
            markers_to_remove = ['RTH2', 'LTH2', 'RLMAL', 'LLMAL', 'RMMAL', 'LMMAL', 'LPSH', 'RPSH', 'C7']
            for marker in markers_to_remove:
                if marker in marker_names:
                    trc_markers.removeColumn(marker)
            marker_names = trc_markers.getColumnLabels()

            rra_time = np.array(rra_markers.getIndependentColumn())
            trc_time = np.array(trc_markers.getIndependentColumn())

            trc_start_index = 0
            trc_end_index = -1
            # Trim trc_time to match time range in rra_time
            if trc_time[0] < rra_time[0]:
                trc_start_index = trc_markers.getNearestRowIndexForTime(rra_time[0])+1
            if trc_time[-1] > rra_time[-1]:
                trc_end_index = trc_markers.getNearestRowIndexForTime(rra_time[-1])-1
            trc_time = trc_time[trc_start_index:trc_end_index]

            # Get vector of indices where trc_time time stamps match rra_time time stamps
            errors = np.zeros((len(trc_time), len(marker_names)))
            for itime, t in enumerate(trc_time):
                trc_row = trc_markers.getRowAtIndex(itime)
                rra_row = rra_markers.getNearestRow(t)
                for imarker, marker_name in enumerate(marker_names):
                    itrc = trc_markers.getColumnIndex(marker_name)
                    irra = rra_markers.getColumnIndex(marker_name)
                    error_vec = np.zeros(3)
                    error_vec[0] = trc_row[itrc][0] / 1000.0 - rra_row[irra][0]
                    error_vec[1] = trc_row[itrc][1] / 1000.0 - rra_row[irra][1]
                    error_vec[2] = trc_row[itrc][2] / 1000.0 - rra_row[irra][2]
                    errors[itime, imarker] = np.linalg.norm(error_vec)

            # Compute RMS for each row in errors and average over all rows
            rms = np.sqrt(np.mean(np.square(errors), axis=1))
            marker_rmse_cycles.append(np.mean(rms))

        marker_rmse[isubj, itrial] = np.mean(marker_rmse_cycles)

    # Compute average marker RMSE for each subject
    marker_rmse_subject[isubj] = np.mean(marker_rmse[isubj, :])

# Save marker_rmse_subject to a CSV file
with open('marker_rmse_rra.csv', 'w') as f:
    f.write('Subject,Marker RMSE (m)\n')
    for subject, rmse in zip(subjects, marker_rmse_subject):
        f.write(f'{subject},{rmse}\n')