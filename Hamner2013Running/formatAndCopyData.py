import pandas as pd
import os
import shutil
import opensim as osim
import xml.etree.ElementTree as ET
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict


# Convenience function to find the gait cycle times for each trial
# using the setup files for the RRA step.
def get_rra_timerange(subject, cycle, ik_tag):

    # Get paths to RRA setup XML files.
    rra_setup = os.path.join('Raw', subject, 'rra_multipleSteps',
                             f'RRA_Results_v191_{ik_tag}',
                             f'{subject}_Setup_RRA_{ik_tag}_cycle{cycle}_v191.xml')
    rra_setup_no_header = os.path.join('Raw', subject, 'rra_multipleSteps',
                                       f'RRA_Results_v191_{ik_tag}',
                                       f'{subject}_Setup_RRA_{ik_tag}_cycle{cycle}_v191_no_header.xml')

    # Strip out the header so we can load the XML file into memory.
    with open(rra_setup) as f:
        with open(rra_setup_no_header, 'w') as f2:
            endheader = 0
            lines = f.readlines()
            for line in lines:
                if line.startswith('<?xml version'):
                    break
                endheader += 1

            f2.writelines(lines[endheader:])

    # Parse the XML file to get the initial and final times for this gait cycle.
    tree = ET.parse(rra_setup_no_header)
    root = tree.getroot()
    itime = float(root[0].find('initial_time').text)
    ftime = float(root[0].find('final_time').text)

    return itime, ftime


# Folder locations. We will reformat and trim the data located
# in the 'Raw' folder and copy it to the 'Formatted' folder.
raw_fpath = os.path.join('Raw')
formatted_fpath = os.path.join('Formatted')

# Load subject demographics.
demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
weights = demographics_df['weight (kg)']
heights = demographics_df['height (m)']

# Process and copy the data!
print('Copying data for AddBiomechanics processing...')
trials = ['run200', 'run300', 'run400', 'run500']
for subject, weight, height in zip(subjects, weights, heights):
    subject_path = os.path.join(formatted_fpath, subject)
    if not os.path.isdir(subject_path):
        os.mkdir(subject_path)

    trials_path = os.path.join(subject_path, 'trials')
    if not os.path.isdir(trials_path): os.mkdir(trials_path)

    # Copy the generic musculoskeletal model.
    model_src = os.path.join(raw_fpath, 'FullBodyModel_SimpleArms_Hamner2010_HPLMarkers.osim')
    model_dst = os.path.join(formatted_fpath, subject, 'unscaled_generic.osim')
    shutil.copyfile(model_src, model_dst)

    # Copy the static trial
    # static_path = os.path.join(trials_path, 'static')
    # if not os.path.isdir(static_path): os.mkdir(static_path)
    # static_src = os.path.join(raw_fpath, subject, 'ExportedData', 'Static_FJC.trc')
    # static_dst = os.path.join(static_path, 'markers.trc')
    # shutil.copyfile(static_src, static_dst)

    # Loop through the trials for this subject.
    for trial in trials:
        print(f'--> {subject}, {trial}')

        trial_path = os.path.join(trials_path, trial)
        if not os.path.isdir(trial_path): os.mkdir(trial_path)

        # If necessary, update the data tags based on the dictionaries above.
        tag = '02'
        if subject in subject_dict.keys():
            for tag_tuple in subject_dict[subject]:
                if tag_tuple[0] == trial:
                    tag = tag_tuple[1]

        data_tag = f'{trial_dict[trial]} {tag}'
        ik_tag = f'{trial_dict[trial]}{tag}'

        # Get the initial time of the first cycle in the trial, and the final time of the
        # last gait cycle in the trial.
        init_cycle = 1
        if subject in init_cycle_dict.keys():
            for cycle_tuple in init_cycle_dict[subject]:
                if cycle_tuple[0] == trial:
                    init_cycle = cycle_tuple[1]

        final_cycle = 3
        if subject in final_cycle_dict.keys():
            for cycle_tuple in final_cycle_dict[subject]:
                if cycle_tuple[0] == trial:
                    final_cycle = cycle_tuple[1]

        initial_time, _ = get_rra_timerange(subject, init_cycle, ik_tag)
        _, final_time = get_rra_timerange(subject, final_cycle, ik_tag)

        # Trim and copy the ground reaction forces.
        grf_src = os.path.join(raw_fpath, subject, 'ExportedData',
                               f'{data_tag}_newCOP3_v24.mot')
        grf_dst = os.path.join(trial_path, 'grf.mot')
        grf = osim.TimeSeriesTable(grf_src)
        grf.trim(initial_time, final_time)
        sto = osim.STOFileAdapter()
        sto.write(grf, grf_dst)

        # Trim and copy the marker trajectories.
        markers_src = os.path.join(raw_fpath, subject, 'ExportedData', f'{data_tag}.trc')
        markers_dst = os.path.join(trial_path, 'markers.trc')
        markers = osim.TimeSeriesTableVec3(markers_src)
        markers.trim(initial_time, final_time)
        # Remove the bad marker from subject17, trial run500
        if subject == 'subject17' and trial == 'run500':
            markers.removeColumn('RTH2')
        trc = osim.TRCFileAdapter()
        trc.write(markers, markers_dst)