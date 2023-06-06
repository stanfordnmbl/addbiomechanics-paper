import pandas as pd
import os
import opensim as osim
import json
import xml.etree.ElementTree as ET
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict


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


if not os.path.isdir(os.path.join('residuals', 'addbio')):
    os.mkdir(os.path.join('residuals', 'addbio'))

addbio_fpath = os.path.join('Processed')
demographics_df = pd.read_csv('demographics.csv')

subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
trials = ['run200', 'run300', 'run400', 'run500']
for subject, mass, height in zip(subjects, masses, heights):
    if not os.path.isdir(os.path.join(addbio_fpath, subject)):
        os.mkdir(os.path.join(addbio_fpath, subject))

    # Create Analysis folder
    analysis_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'Analysis')
    if not os.path.isdir(analysis_fpath):
        os.mkdir(analysis_fpath)

    # Loop over all trials for this subject
    for trial in trials:

        # File paths
        grf_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'ID', f'{trial}_grf.mot')
        id_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'ID', f'{trial}_id.sto')

        # Get start and end times for AnalyzeTool
        table = osim.TimeSeriesTable(id_fpath)
        time = table.getIndependentColumn()
        startTime = time[0]
        endTime = time[table.getNumRows()-1]

        # Fill and write Analysis setup file template
        template_fpath = os.path.join('setup_analysis.xml')
        setup_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'Analysis',
                                   f'{subject}_{trial}_setupAnalysis.xml')

        model_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'Models', 'final.osim')
        results_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'Analysis', f'results_{trial}')
        coordinates_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot')
        extloads_fpath = os.path.join(addbio_fpath, subject, 'osim_results', 'ID', f'{trial}_external_forces.xml')
        fill_analysis_template(
            template_fpath, setup_fpath, trial,
            os.path.relpath(model_fpath, analysis_fpath),
            os.path.relpath(results_fpath, analysis_fpath),
            startTime, endTime,
            os.path.relpath(extloads_fpath, analysis_fpath),
            os.path.relpath(coordinates_fpath, analysis_fpath))

        # Run Analysis to compute center of mass trajectories
        analyze = osim.AnalyzeTool(setup_fpath)
        analyze.run()

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
        for cycle, cycle_dict in zip(cycles, cycle_dicts):
            # update cycle number, if needed
            if subject in cycle_dict.keys():
                for cycle_tuple in cycle_dict[subject]:
                    if cycle_tuple[0] == trial:
                        cycle = cycle_tuple[1]

            initial_time, final_time = get_rra_timerange(subject, cycle, ik_tag)

            # Load files
            grf = osim.TimeSeriesTable(grf_fpath)
            id = osim.TimeSeriesTable(id_fpath)
            com = osim.TimeSeriesTable(os.path.join(results_fpath, f'analysis_{trial}_BodyKinematics_pos_global.sto'))

            # Trim time ranges
            grf.trim(initial_time, final_time)
            id.trim(initial_time, final_time)
            com.trim(initial_time, final_time)

            # Write all files
            sto = osim.STOFileAdapter()
            sto.write(grf, os.path.join('residuals', 'addbio', f'{subject}_{trial}_cycle{cycle}_grf.mot'))
            sto.write(id, os.path.join('residuals', 'addbio', f'{subject}_{trial}_cycle{cycle}_residuals.sto'))
            sto.write(com, os.path.join('residuals', 'addbio', f'{subject}_{trial}_cycle{cycle}_com.sto'))