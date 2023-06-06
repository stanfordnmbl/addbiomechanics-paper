import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import plotIKResults, plotIDResults
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict


def interp(df, new_index):
    """Return a new DataFrame with all columns values interpolated
    to the new_index values."""
    df_out = pd.DataFrame(index=new_index)
    df_out.index.name = df.index.name

    for colname, col in df.items():
        df_out[colname] = np.interp(new_index, df.index, col)

    return df_out


def compute_continuous_rms_error(col1, col2, time):
    """Compute the continuous RMS error between two columns of data."""
    time_interval = time[1] - time[0]
    duration = time[time.size-1] - time[0]
    error = (180 / 3.14159) * (col1 - col2)
    squared_error = error ** 2
    integral_sum_squared_error = time_interval * 0.5 * (squared_error.sum() + squared_error[1:-1].sum())
    return np.sqrt(integral_sum_squared_error) / duration


def compute_mean_absolute_error(col1, col2, scale=1.0):
    error = scale * (col1 - col2)
    return np.mean(np.abs(error))


demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
trials = ['run200', 'run300', 'run400', 'run500']
markfit_fpath = os.path.join('Processed', 'marker_fitting_only')
dynfit_fpath = os.path.join('Processed', 'dynamics_fitting')
rad2deg = 180 / 3.14159

rms_ik_errors = dict()
rms_id_errors = dict()
if not os.path.isdir(os.path.join('Processed', 'comparison')):
    os.mkdir(os.path.join('Processed', 'comparison'))
for subject, mass, height in zip(subjects, masses, heights):
    if not os.path.isdir(os.path.join('Processed', 'comparison', subject)):
        os.mkdir(os.path.join('Processed', 'comparison', subject))

    if not os.path.isdir(os.path.join('Processed', 'comparison', subject, 'IK')):
        os.mkdir(os.path.join('Processed', 'comparison', subject, 'IK'))
    if not os.path.isdir(os.path.join('Processed', 'comparison', subject, 'ID')):
        os.mkdir(os.path.join('Processed', 'comparison', subject, 'ID'))

    # Loop over all trials for this subject
    for trial in trials:
        # update data tags, if needed
        tag = '02'
        if subject in subject_dict.keys():
            for tag_tuple in subject_dict[subject]:
                if tag_tuple[0] == trial:
                    tag = tag_tuple[1]

        data_tag = f'{trial_dict[trial]} {tag}'
        ik_tag = f'{trial_dict[trial]}{tag}'

        # IK results
        # ----------
        data_fpaths = list()
        header_shifts = list()
        data_fpaths.append(os.path.join(dynfit_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot'))
        data_fpaths.append(os.path.join(markfit_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot'))
        header_shifts.append(-1)
        header_shifts.append(-1)

        # Plot RRA results from Sam's study
        cycle_dicts = [init_cycle_dict, second_cycle_dict, final_cycle_dict]
        cycles = [1, 2, 3]
        for cycle, cycle_dict in zip(cycles, cycle_dicts):
            # update cycle number, if needed
            if subject in cycle_dict.keys():
                for cycle_tuple in cycle_dict[subject]:
                    if cycle_tuple[0] == trial:
                        cycle = cycle_tuple[1]

            cycle_fpath = os.path.join('Raw', subject, 'rra_multipleSteps', f'RRA_Results_v191_{ik_tag}',
                                         f'RRA_Results_v191_{ik_tag}_cycle{cycle}',
                                         f'{subject}_{ik_tag}_cycle{cycle}_states.sto')
            data_fpaths.append(cycle_fpath)
            header_shifts.append(1)

        dynfit, refs = plotIKResults(data_fpaths,
                          os.path.join('Processed', 'comparison', subject, 'IK', f'{trial}_ik.pdf'),
                          header_shifts)
        markfit = refs[0]

        # Stack the dataframes in refs[:1] into a single dataframe
        rra = pd.concat(refs[1:], axis=0)
        rra = rra.reset_index(drop=True)
        rra = rra.drop_duplicates(subset='time')

        # Round the values in rra['time'] to the nearest 0.01
        rra['time'] = np.round(rra['time'], 2)
        rra = rra.drop_duplicates(subset='time')
        rra = rra.reset_index(drop=True)

        # Set the index of dynfit, markfit, and rra to be time
        dynfit = dynfit.set_index('time')
        markfit = markfit.set_index('time')
        rra = rra.set_index('time')

        # Keep only the time values that are in all three dataframes
        time = dynfit.index.intersection(markfit.index).intersection(rra.index)
        dynfit = dynfit.loc[time]
        markfit = markfit.loc[time]
        rra = rra.loc[time]

        # Interpolate the dataframes to the time values in rra['time']
        # dynfit = interp(dynfit, rra.index)
        # markfit = interp(markfit, rra.index)

        # Compute RMS differences between columns in markfit and dynfit
        rms_ik = pd.DataFrame(index=markfit.columns, columns=['mark_v_rra', 'mark_v_dyn', 'dyn_v_rra'])
        for col in markfit.columns:
            rms_ik.loc[col, 'mark_v_dyn'] = compute_mean_absolute_error(markfit[col], dynfit[col], scale=rad2deg)
            rms_ik.loc[col, 'mark_v_rra'] = compute_mean_absolute_error(markfit[col], rra[col], scale=rad2deg)
            rms_ik.loc[col, 'dyn_v_rra'] = compute_mean_absolute_error(dynfit[col], rra[col], scale=rad2deg)

        # Drop subtalar, mtp, wrist_dev, and wrist_flex rows
        rms_ik = rms_ik.drop(['subtalar_angle_r', 'subtalar_angle_l', 'mtp_angle_r', 'mtp_angle_l',
                        'wrist_flex_r', 'wrist_flex_l', 'wrist_dev_r', 'wrist_dev_l'])

        # Average results in rms for indices that end in '_r' and '_l'
        rms_ik = rms_ik.groupby(rms_ik.index.str[:-2]).mean()

        # Plot rms in bar chart
        fig, ax = plt.subplots()
        rms_ik.plot.bar(ax=ax)
        fig.set_size_inches(10, 8)
        plt.xticks(rotation=90)
        ax.set_ylabel('RMS error (deg)')
        ax.set_xlabel('Coordinate')
        ax.set_title(f'Joint angle RMS differences for {subject} {trial} (mean +/- std)')
        fig.tight_layout()
        fig.savefig(os.path.join('Processed', 'comparison', subject, 'IK', f'{trial}_rms.pdf'))
        plt.close(fig)

        # Add to dictionary
        rms_ik_errors[f'{subject}_{trial}'] = rms_ik

        # ID results
        # ----------
        data_fpaths = list()
        header_shifts = list()
        data_fpaths.append(os.path.join(dynfit_fpath, subject, 'osim_results', 'ID', f'{trial}_id.sto'))
        header_shifts.append(-1)

        # Plot RRA results from Sam's study
        cycle_dicts = [init_cycle_dict, second_cycle_dict, final_cycle_dict]
        cycles = [1, 2, 3]
        for cycle, cycle_dict in zip(cycles, cycle_dicts):
            # update cycle number, if needed
            if subject in cycle_dict.keys():
                for cycle_tuple in cycle_dict[subject]:
                    if cycle_tuple[0] == trial:
                        cycle = cycle_tuple[1]

            cycle_fpath = os.path.join('Raw', subject, 'rra_multipleSteps', f'RRA_Results_v191_{ik_tag}',
                                       f'RRA_Results_v191_{ik_tag}_cycle{cycle}',
                                       f'{subject}_{ik_tag}_cycle{cycle}_Actuation_force.sto')
            data_fpaths.append(cycle_fpath)
            header_shifts.append(-5)

        dynfit, refs = plotIDResults(data_fpaths,
                                     os.path.join('Processed', 'comparison', subject, 'ID', f'{trial}_id.pdf'),
                                     header_shifts)

        # Stack the dataframes in refs[:1] into a single dataframe
        rra = pd.concat(refs, axis=0)
        rra = rra.reset_index(drop=True)
        rra = rra.drop_duplicates(subset='time')

        # Round the values in rra['time'] to the nearest 0.01
        rra['time'] = np.round(rra['time'], 2)
        rra = rra.drop_duplicates(subset='time')
        rra = rra.reset_index(drop=True)

        # Set the index of dynfit, markfit, and rra to be time
        dynfit = dynfit.set_index('time')
        rra = rra.set_index('time')

        # Keep only the time values that are in all three dataframes
        time = dynfit.index.intersection(rra.index)
        dynfit = dynfit.loc[time]
        rra = rra.loc[time]


        # Compute RMS differences between columns in markfit and dynfit
        rms_id = pd.DataFrame(index=dynfit.columns, columns=['dyn_v_rra'])
        for col in dynfit.columns:
            rms_id.loc[col, 'dyn_v_rra'] = compute_mean_absolute_error(dynfit[col], rra[col])

        # Average results in rms for indices that end in '_r' and '_l'
        rms_id = rms_id.groupby(rms_id.index.str[:-2]).mean()

        # Plot rms in bar chart
        fig, ax = plt.subplots()
        rms_id.plot.bar(ax=ax)
        fig.set_size_inches(10, 8)
        plt.xticks(rotation=90)
        ax.set_ylabel('RMS error (N-m)')
        ax.set_xlabel('Coordinate')
        ax.set_title(f'Joint torque RMS differences for {subject} {trial} (mean +/- std)')
        fig.tight_layout()
        fig.savefig(os.path.join('Processed', 'comparison', subject, 'ID', f'{trial}_rms.pdf'))
        plt.close(fig)

        # Add to dictionary
        rms_id_errors[f'{subject}_{trial}'] = rms_id



# Compute mean and standard deviation of RMS differences of all trials in rms_ik_errors
rms_mean = pd.DataFrame(index=rms_ik_errors['subject01_run200'].index, columns=['mark_v_dyn', 'mark_v_rra', 'dyn_v_rra'])
rms_std = pd.DataFrame(index=rms_ik_errors['subject01_run200'].index, columns=['mark_v_dyn', 'mark_v_rra', 'dyn_v_rra'])

for index in rms_ik_errors['subject01_run200'].index:
    for col in rms_mean.columns:
        rms_mean.loc[index, col] = np.mean([rms_ik_errors[key].loc[index, col] for key in rms_ik_errors.keys()])
        rms_std.loc[index, col] = np.std([rms_ik_errors[key].loc[index, col] for key in rms_ik_errors.keys()])

rms_mean.plot.bar(rot=0, yerr=rms_std)
fig = plt.gcf()
fig.set_size_inches(12, 5)
plt.xticks(rotation=90)
plt.title(f'Joint angle RMS differences between methods (mean +/- std)')
plt.ylabel('RMS difference (deg)')
plt.tight_layout()
plt.savefig(os.path.join('Processed', 'comparison', 'mean_rms_ik.pdf'))
plt.close()

# Compute mean and standard deviation of RMS differences of all trials in rms_id_errors
rms_mean = pd.DataFrame(index=rms_id_errors['subject01_run200'].index, columns=['dyn_v_rra'])
rms_std = pd.DataFrame(index=rms_id_errors['subject01_run200'].index, columns=['dyn_v_rra'])

for index in rms_id_errors['subject01_run200'].index:
    for col in rms_mean.columns:
        rms_mean.loc[index, col] = np.mean([rms_id_errors[key].loc[index, col] for key in rms_id_errors.keys()])
        rms_std.loc[index, col] = np.std([rms_id_errors[key].loc[index, col] for key in rms_id_errors.keys()])

rms_mean.plot.bar(rot=0, yerr=rms_std)
fig = plt.gcf()
fig.set_size_inches(12, 5)
plt.xticks(rotation=90)
plt.title(f'Joint torque RMS differences between methods (mean +/- std)')
plt.ylabel('RMS difference (deg)')
plt.tight_layout()
plt.savefig(os.path.join('Processed', 'comparison', 'mean_rms_id.pdf'))
plt.close()
