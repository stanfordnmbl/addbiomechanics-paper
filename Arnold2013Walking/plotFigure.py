import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import storage2pandas
from helpers import remove_columns_not_in_both
import json

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['mathtext.rm'] = 'serif'


# Add errorbars to a bar chart. For positive values, the errorbars will
# be above the bars, and for negative values, the errorbars will be
# below the bars.
def plot_errorbar(ax, x, y, yerr):
    lolims = y > 0
    uplims = y < 0
    ple, cle, ble = ax.errorbar(x, y, yerr=yerr,
        fmt='none', ecolor='black',
        capsize=0, solid_capstyle='projecting', lw=1.0,
        zorder=2.5, clip_on=False, lolims=lolims, uplims=uplims,
        elinewidth=0.4, markeredgewidth=0.4)
    for cl in cle:
        cl.set_marker('_')
        cl.set_markersize(8)


demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
trials = ['walk2']
processed_fpath = os.path.join('Processed')

rad2deg = 180 / 3.14159
ik_rms_errors = np.zeros(len(subjects))
id_rms_errors = np.zeros(len(subjects))
marker_rmse = np.zeros(len(subjects))
for isubj, (subject, mass, height) in enumerate(zip(subjects, masses, heights)):

    # Loop over all trials for this subject
    for trial in trials:

        # Inverse kinematics results
        # --------------------------
        processed_ik = storage2pandas(os.path.join(processed_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot'),
                                   header_shift=-1)
        coordinates = storage2pandas(os.path.join('ID', subject, 'coordinates.sto'), header_shift=1)
        coordinates, processed_ik = remove_columns_not_in_both(coordinates, processed_ik)

        # Drop subtalar, mtp, pro_sup, and translational coordinate columns.
        columns_to_drop = ['mtp_angle_r', 'mtp_angle_l', 'pro_sup_r', 'pro_sup_l',
                           'pelvis_tx', 'pelvis_ty', 'pelvis_tz']
        coordinates = coordinates.drop(columns=columns_to_drop)
        processed_ik = processed_ik.drop(columns=columns_to_drop)

        # Compute error between coordinates and dynfit_ik.
        ik_error = processed_ik - coordinates
        ik_error = ik_error.drop(columns=['time'])
        ik_error = ik_error * rad2deg

        # Compute RMS for each row in 'error'.
        ik_rms = ik_error.apply(lambda x: np.sqrt(np.mean(x**2)), axis=1)

        # Average and append to list.
        ik_rms_errors[isubj] = ik_rms.mean()

        # Inverse dynamics results
        # ------------------------
        processed_id = storage2pandas(os.path.join(processed_fpath, subject, 'osim_results', 'ID', f'{trial}_id.sto'),
                                   header_shift=-1)
        original_id = storage2pandas(os.path.join('ID', subject, 'inverse_dynamics.sto'), header_shift=1)
        original_id, processed_id = remove_columns_not_in_both(original_id, processed_id)

        # Drop subtalar, mtp, pro_sup, and translational coordinate columns.
        columns_to_drop = ['pro_sup_r_moment', 'pro_sup_l_moment', 'mtp_angle_r_moment', 'mtp_angle_l_moment',
                           'pelvis_tilt_moment', 'pelvis_list_moment', 'pelvis_rotation_moment',
                           'pelvis_tx_force', 'pelvis_ty_force', 'pelvis_tz_force',
                           'wrist_dev_l_moment', 'wrist_flex_l_moment', 'wrist_dev_r_moment', 'wrist_flex_r_moment']
        processed_id = processed_id.drop(columns=columns_to_drop)
        original_id = original_id.drop(columns=columns_to_drop)

        # Compute error between id and dynfit_id.
        BW = mass * 9.81
        id_error = 100.0 * (processed_id - original_id) / (BW * height)
        id_error = id_error.drop(columns=['time'])

        # Compute RMS for each row in 'error'.
        id_rms = id_error.apply(lambda x: np.sqrt(np.mean(x**2)), axis=1)

        # Average and append to list.
        id_rms_errors[isubj] = id_rms.mean()

        # Marker errors
        # -------------
        results_fpath = os.path.join('Processed', subject, '_results.json')
        f = open(results_fpath)
        results = json.load(f)
        marker_rmse[isubj] = 100.0*results['autoAvgRMSE']


# Create a figure with four subplots.
fig = plt.figure(figsize=(9, 4))
gs = fig.add_gridspec(1, 13, left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2)
axes = list()
axes.append(fig.add_subplot(gs[0, 0:2]))
axes.append(fig.add_subplot(gs[0, 3:5]))
axes.append(fig.add_subplot(gs[0, 6:8]))
axes.append(fig.add_subplot(gs[0, 9:13]))

# Plot the RMS errors for inverse kinematics with error bars
# representing the standard deviation.
ylabel_fs = 8
xlabel_fs = 9
yticklabel_fs = 7
colors_fpath = os.path.join('..', 'colors.json')
f = open(colors_fpath)
colors = json.load(f)
color = colors['addbio']
width = 0.3
axes[0].bar(0, np.mean(ik_rms_errors), width, color=color)
plot_errorbar(axes[0], 0, np.mean(ik_rms_errors), np.std(ik_rms_errors))
# axes[0].set_title('Joint angle error')
axes[0].set_ylabel(r'Average RMS error $[^\circ]$', fontsize=ylabel_fs)
axes[0].set_xticks([0])
axes[0].set_xticklabels(['Joint angle\nerror'], fontsize=xlabel_fs)
axes[0].set_ylim([0, 2])
axes[0].set_yticks([0, 0.5, 1, 1.5, 2])
axes[0].set_yticklabels([0, 0.5, 1, 1.5, 2], fontsize=yticklabel_fs)
axes[0].set_xlim([-0.3, 0.3])

# Plot the RMS errors for inverse dynamics.
axes[1].bar(0, np.mean(id_rms_errors), width, color=color)
plot_errorbar(axes[1], 0, np.mean(id_rms_errors), np.std(id_rms_errors))
# axes[1].set_title('Joint moment error')
axes[1].set_ylabel(r'Average RMS error $[\% BW*ht]$', fontsize=ylabel_fs)
axes[1].set_xticks([0])
axes[1].set_xticklabels(['Joint moment\nerror'], fontsize=xlabel_fs)
axes[1].set_ylim([0, 2.0])
axes[1].set_yticks([0, 0.5, 1, 1.5, 2])
axes[1].set_yticklabels([0, 0.5, 1, 1.5, 2], fontsize=yticklabel_fs)
axes[1].set_xlim([-0.3, 0.3])

# Plot the marker RMSE.
axes[2].bar(0, np.mean(marker_rmse), width, color=color)
plot_errorbar(axes[2], 0, np.mean(marker_rmse), np.std(marker_rmse))
# axes[2].set_title('Marker RMSE')
axes[2].set_ylabel(r'Average RMS error $[cm]$', fontsize=ylabel_fs)
axes[2].set_xticks([0])
axes[2].set_xticklabels(['Marker error'], fontsize=xlabel_fs)
axes[2].set_ylim([0, 2.0])
axes[2].set_yticks([0, 0.5, 1, 1.5, 2])
axes[2].set_yticklabels([0, 0.5, 1, 1.5, 2], fontsize=yticklabel_fs)
axes[2].set_xlim([-0.3, 0.3])

# Plot the residuals
residuals_df = pd.read_csv('residuals_addbio.csv')
mean_rms_forces_addbio = 100.0*residuals_df['kinetic_normalized_rms_forces'].mean()
mean_rms_moments_addbio = 100.0*residuals_df['kinetic_normalized_rms_moments'].mean()
std_rms_forces_addbio = 100.0*residuals_df['kinetic_normalized_rms_forces'].std()
std_rms_moments_addbio = 100.0*residuals_df['kinetic_normalized_rms_moments'].std()
axes[3].bar(0, mean_rms_forces_addbio, width, color=color)
axes[3].bar(0.6, mean_rms_moments_addbio, width, color=color)
plot_errorbar(axes[3], 0, mean_rms_forces_addbio, std_rms_forces_addbio)
plot_errorbar(axes[3], 0.6, mean_rms_moments_addbio, std_rms_moments_addbio)
# axes[3].set_title('Residuals')
axes[3].set_ylabel(r'Average RMS residual load $[\%]$', fontsize=ylabel_fs)
axes[3].set_xticks([0, 0.6])
axes[3].set_xticklabels(['Residual\nforce', 'Residual\ntorque'], fontsize=xlabel_fs)
axes[3].set_ylim([0, 2.0])
axes[3].set_yticks([0, 0.5, 1, 1.5, 2])
axes[3].set_yticklabels([0, 0.5, 1, 1.5, 2], fontsize=yticklabel_fs)
axes[3].set_xlim([-0.3, 0.9])

# Remove top and right spines.
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Save figure.
# fig.tight_layout()
fig.savefig('figures/joints_markers_and_residuals.png', dpi=500, bbox_inches='tight')

print('Joint angle error: mean = %f, std = %f' % (np.mean(ik_rms_errors), np.std(ik_rms_errors)))
print('Joint moment error: mean = %f, std = %f' % (np.mean(id_rms_errors), np.std(id_rms_errors)))
print('Marker RMSE: mean = %f, std = %f' % (np.mean(marker_rmse), np.std(marker_rmse)))
print('Residual force: mean = %f, std = %f' % (mean_rms_forces_addbio, std_rms_forces_addbio))
print('Residual moment: mean = %f, std = %f' % (mean_rms_moments_addbio, std_rms_moments_addbio))