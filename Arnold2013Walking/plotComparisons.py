import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import plotIKResults, plotIDResults
from helpers import remove_columns_not_in_both


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
trials = ['walk2']
processed_fpath = os.path.join('Processed')

rms_ik_errors = dict()
rms_id_errors = dict()
if not os.path.isdir(os.path.join('figures', 'comparison')):
    os.mkdir(os.path.join('figures', 'comparison'))
for subject, mass, height in zip(subjects, masses, heights):
    if not os.path.isdir(os.path.join('figures', 'comparison', subject)):
        os.mkdir(os.path.join('figures', 'comparison', subject))
    if not os.path.isdir(os.path.join('figures', 'comparison', subject, 'IK')):
        os.mkdir(os.path.join('figures', 'comparison', subject, 'IK'))
    if not os.path.isdir(os.path.join('figures', 'comparison', subject, 'ID')):
        os.mkdir(os.path.join('figures', 'comparison', subject, 'ID'))

    # Loop over all trials for this subject
    for trial in trials:

        # IK results
        # ----------
        data_fpaths = list()
        header_shifts = list()
        data_fpaths.append(os.path.join(processed_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot'))
        data_fpaths.append(os.path.join('ID', subject, 'coordinates.sto'))
        header_shifts.append(-1)
        header_shifts.append(1)

        processed, refs = plotIKResults(data_fpaths,
                          os.path.join('figures', 'comparison', subject, 'IK', f'{trial}_ik.pdf'),
                          header_shifts)
        original = refs[0]

        # Compute RMS differences between columns in the addbio results and the original results
        rms_ik = pd.DataFrame(index=processed.columns, columns=['addbio_vs_original'])
        rad2deg = 180 / 3.14159
        for col in processed.columns:
            rms_ik.loc[col, 'addbio_vs_original'] = compute_mean_absolute_error(
                processed[col], original[col], scale=rad2deg)

        # Drop subtalar, mtp, and pro_sup columns
        rms_ik = rms_ik.drop(['subtalar_angle_r', 'subtalar_angle_l',
                              'mtp_angle_r', 'mtp_angle_l',
                              'pro_sup_r', 'pro_sup_l',
                              'arm_rot_r', 'arm_rot_l'])

        # Plot rms in bar chart
        fig, ax = plt.subplots()
        rms_ik.plot.bar(ax=ax)
        fig.set_size_inches(10, 8)
        plt.xticks(rotation=90)
        ax.set_ylabel('RMS error (deg)')
        ax.set_xlabel('Coordinate')
        ax.set_title(f'Joint angle mean absolute error for {subject} {trial} (mean +/- std)')
        fig.tight_layout()
        fig.savefig(os.path.join('figures', 'comparison', subject, 'IK', f'{trial}_rms.pdf'))
        plt.close(fig)

        # Add to dictionary
        rms_ik_errors[f'{subject}_{trial}'] = rms_ik

        # ID results
        # ----------
        data_fpaths = list()
        header_shifts = list()
        data_fpaths.append(os.path.join(processed_fpath, subject, 'osim_results', 'ID', f'{trial}_id.sto'))
        data_fpaths.append(os.path.join('ID', subject, 'inverse_dynamics.sto'))
        header_shifts.append(-1)
        header_shifts.append(1)

        processed, refs = plotIDResults(data_fpaths,
                            os.path.join('figures', 'comparison', subject, 'ID', f'{trial}_id.pdf'),
                            header_shifts)
        original = refs[0]

        # Compute RMS differences between columns in markfit and dynfit
        rms_id = pd.DataFrame(index=processed.columns, columns=['addbio_vs_original'])
        for col in processed.columns:
            rms_id.loc[col, 'addbio_vs_original'] = compute_mean_absolute_error(processed[col], original[col])

        # Drop subtalar, mtp, and pro_sup columns
        rms_id = rms_id.drop(['pro_sup_r_moment', 'pro_sup_l_moment'])

        # Plot rms in bar chart
        fig, ax = plt.subplots()
        rms_id.plot.bar(ax=ax)
        fig.set_size_inches(10, 8)
        plt.xticks(rotation=90)
        ax.set_ylabel('RMS error (N-m)')
        ax.set_xlabel('Coordinate')
        ax.set_title(f'Joint torque mean absolute error for {subject} {trial} (mean +/- std)')
        fig.tight_layout()
        fig.savefig(os.path.join('figures', 'comparison', subject, 'ID', f'{trial}_rms.pdf'))
        plt.close(fig)

        # Add to dictionary
        rms_id_errors[f'{subject}_{trial}'] = rms_id

# Compute mean and standard deviation of RMS differences of all trials in rms_ik_errors
first_dict_index = list(rms_ik_errors.keys())[0]
rms_ik_mean = pd.DataFrame(index=rms_ik_errors[first_dict_index].index, columns=['addbio_vs_original'])
rms_ik_std = pd.DataFrame(index=rms_ik_errors[first_dict_index].index, columns=['addbio_vs_original'])
for index in rms_ik_errors[first_dict_index].index:
    for col in rms_ik_mean.columns:
        rms_ik_mean.loc[index, col] = np.mean([rms_ik_errors[key].loc[index, col] for key in rms_ik_errors.keys()])
        rms_ik_std.loc[index, col] = np.std([rms_ik_errors[key].loc[index, col] for key in rms_ik_errors.keys()])

rms_ik_mean.plot.bar(rot=0, yerr=rms_ik_std)
fig = plt.gcf()
fig.set_size_inches(12, 5)
plt.xticks(rotation=90)
plt.title(f'Joint angle mean absolute error (mean +/- std)')
plt.ylabel('RMS difference (deg)')
plt.tight_layout()
plt.savefig(os.path.join('figures', 'comparison', 'mean_rms_ik.pdf'))
plt.close()

# Compute mean and standard deviation of RMS differences of all trials in rms_id_errors
rms_id_mean = pd.DataFrame(index=rms_id_errors[first_dict_index].index, columns=['addbio_vs_original'])
rms_id_std = pd.DataFrame(index=rms_id_errors[first_dict_index].index, columns=['addbio_vs_original'])
for index in rms_id_errors[first_dict_index].index:
    for col in rms_id_mean.columns:
        rms_id_mean.loc[index, col] = np.mean([rms_id_errors[key].loc[index, col] for key in rms_id_errors.keys()])
        rms_id_std.loc[index, col] = np.std([rms_id_errors[key].loc[index, col] for key in rms_id_errors.keys()])

rms_id_mean.plot.bar(rot=0, yerr=rms_id_std)
fig = plt.gcf()
fig.set_size_inches(12, 5)
plt.xticks(rotation=90)
plt.title(f'Joint torque mean absolute error (mean +/- std)')
plt.ylabel('RMS difference (N-m)')
plt.tight_layout()
plt.savefig(os.path.join('figures', 'comparison', 'mean_rms_id.pdf'))
plt.close()
