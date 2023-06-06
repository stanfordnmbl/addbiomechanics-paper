import pandas as pd
import os
import shutil
import opensim as osim
import xml.etree.ElementTree as ET
import json
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict


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


if not os.path.isdir(os.path.join('residuals', 'hamner')):
    os.mkdir(os.path.join('residuals', 'hamner'))

hamner_results_dir = os.path.join('residuals', 'hamner', 'results')
if not os.path.isdir(hamner_results_dir):
    os.mkdir(hamner_results_dir)

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
weights = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
trials = ['run200', 'run300', 'run400', 'run500']

print('Copying original data to compute residuals...')
for subject, weight, height in zip(subjects, weights, heights):
    subject_path = os.path.join('residuals', 'hamner', 'results', subject)
    if not os.path.isdir(subject_path):
        os.mkdir(subject_path)

    trials_path = os.path.join(subject_path, 'trials')
    if not os.path.isdir(trials_path): os.mkdir(trials_path)

    # copy model
    model_src = os.path.join('Raw', subject, 'scale', f'{subject}_scaled_v191_40.osim')
    model_dst = os.path.join(hamner_results_dir, subject, 'model.osim')
    shutil.copyfile(model_src, model_dst)

    for trial in trials:
        # Ignore trials with missing GRFs
        f = open('ignored_trials.json')
        data = json.load(f)
        if subject in data:
            if trial in data[subject]:
                continue

        trial_path = os.path.join(trials_path, trial)
        if not os.path.isdir(trial_path): os.mkdir(trial_path)

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
            grf_fpath = os.path.join('Raw', subject, 'ExportedData',
                                     f'{data_tag}_newCOP3_v24.mot')
            grf = osim.TimeSeriesTable(grf_fpath)

            rra_fpath = os.path.join('Raw', subject, 'rra_multipleSteps', f'RRA_Results_v191_{ik_tag}',
                                     f'RRA_Results_v191_{ik_tag}_cycle{cycle}',
                                     f'{subject}_{ik_tag}_cycle{cycle}_Actuation_force.sto')
            rra = osim.TimeSeriesTable(rra_fpath)

            coords_fpath = os.path.join('Raw', subject, 'rra_multipleSteps', f'RRA_Results_v191_{ik_tag}',
                                        f'RRA_Results_v191_{ik_tag}_cycle{cycle}',
                                        f'{subject}_{ik_tag}_cycle{cycle}_Kinematics_q.sto')
            coords = osim.TimeSeriesTable(coords_fpath)

            # com = osim.TimeSeriesTable(os.path.join(results_fpath, f'analysis_{trial}_BodyKinematics_pos_global.sto'))

            # Trim time ranges
            grf.trim(initial_time, final_time)
            # com.trim(initial_time, final_time)

            # Write all files
            sto = osim.STOFileAdapter()
            sto.write(grf, os.path.join('residuals', 'hamner', f'{subject}_{trial}_cycle{cycle}_grf.mot'))
            sto.write(rra, os.path.join('residuals', 'hamner', f'{subject}_{trial}_cycle{cycle}_residuals.sto'))
            sto.write(coords, os.path.join('residuals', 'hamner', 'results', subject, 'trials', trial,
                                           f'{subject}_{trial}_cycle{cycle}_coordinates.sto'))
            # sto.write(com, os.path.join('residuals', 'addbio', f'{subject}_{trial}_cycle{cycle}_com.sto'))
