import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import storage2pandas
import json

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['mathtext.rm'] = 'serif'
color_opencap = '#2e2e2e'
color_addbio = '#7798ce'

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
opencap_fpath = os.path.join('residuals', 'opencap')
addbio_fpath = os.path.join('residuals', 'addbio')

rad2deg = 180 / 3.14159
marker_rmse_addbio = np.zeros(len(subjects))
marker_rmse_opencap = np.zeros(len(subjects))
trials = ['DJ', 'squats1']
trial_names = ['Drop Jump', 'Squats']
coordsToPlot = ['hip_flexion_r', 'knee_angle_r', 'ankle_angle_r']
joint_angles_opencap = dict()
joint_angles_addbio = dict()
joint_torques_opencap = dict()
joint_torques_addbio = dict()
N = 201
Nsub = 77
for trial in trials:
    joint_angles_opencap[trial] = np.zeros((N, len(coordsToPlot), len(subjects)))
    joint_angles_addbio[trial] = np.zeros((N, len(coordsToPlot), len(subjects)))
    joint_torques_opencap[trial] = np.zeros((N, len(coordsToPlot), len(subjects)))
    joint_torques_addbio[trial] = np.zeros((N, len(coordsToPlot), len(subjects)))

for isubj, (subject, mass) in enumerate(zip(subjects, masses)):

    # Loop over all trials for this subject
    for itrial, trial in enumerate(trials):

        trial_tag = trial
        if trial == 'DJ':
            if os.path.isdir(os.path.join('Formatted', subject, 'trials', 'DJ1')):
                trial_tag = 'DJ1'
            elif os.path.isdir(os.path.join('Formatted', subject, 'trials', 'DJ2')):
                trial_tag = 'DJ2'
            elif os.path.isdir(os.path.join('Formatted', subject, 'trials', 'DJ3')):
                trial_tag = 'DJ3'
            elif os.path.isdir(os.path.join('Formatted', subject, 'trials', 'DJ4')):
                trial_tag = 'DJ4'
            elif os.path.isdir(os.path.join('Formatted', subject, 'trials', 'DJ5')):
                trial_tag = 'DJ5'

        # Joint angles
        # ------------
        coordinates_addbio_fpath = os.path.join('Processed', subject, 'osim_results', 'IK',
                                                f'{trial_tag}_ik.mot')
        coordinates_addbio = osim.TimeSeriesTable(coordinates_addbio_fpath)
        time_addbio = np.array(coordinates_addbio.getIndependentColumn())

        coordinates_opencap_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'IK', f'{trial_tag}.mot')
        coordinates_opencap = osim.TimeSeriesTable(coordinates_opencap_fpath)
        time_opencap = np.array(coordinates_opencap.getIndependentColumn())

        # Find the intersection of the time ranges in time_addbio and time_opencap
        time = np.intersect1d(time_addbio, time_opencap)
        coordinates_addbio.trim(time[0], time[-1])
        coordinates_opencap.trim(time[0], time[-1])

        for icoord, coordToPlot in enumerate(coordsToPlot):
            coord = rad2deg * coordinates_addbio.getDependentColumn(coordToPlot).to_numpy()
            time_interp = np.linspace(time[0], time[-1], N)
            joint_angles_addbio[trial][:, icoord, isubj] = np.interp(time_interp, time, coord)

        for icoord, coordToPlot in enumerate(coordsToPlot):
            coord = coordinates_opencap.getDependentColumn(coordToPlot).to_numpy()
            time_interp = np.linspace(time[0], time[-1], N)
            joint_angles_opencap[trial][:, icoord, isubj] = np.interp(time_interp, time, coord)

        # Joint torques
        # -------------
        torques_addbio_fpath = os.path.join('Processed', subject, 'osim_results', 'ID', f'{trial_tag}_id.sto')
        torques_addbio = osim.TimeSeriesTable(torques_addbio_fpath)
        time_addbio = np.array(torques_addbio.getIndependentColumn())
        torques_opencap_fpath = os.path.join('Raw', subject, 'OpenSimData', 'Mocap', 'ID', f'{trial_tag}.sto')
        torques_opencap = osim.TimeSeriesTable(torques_opencap_fpath)
        time_opencap = np.array(torques_opencap.getIndependentColumn())

        # Find the intersection of the time ranges in time_addbio and time_opencap
        time = np.intersect1d(time_addbio, time_opencap)
        torques_addbio.trim(time[0], time[-1])
        torques_opencap.trim(time[0], time[-1])

        for icoord, coordToPlot in enumerate(coordsToPlot):
            coord = torques_addbio.getDependentColumn(f'{coordToPlot}_moment').to_numpy() / mass
            time_interp = np.linspace(time[0], time[-1], N)
            joint_torques_addbio[trial][:, icoord, isubj] = np.interp(time_interp, time, coord)

        for icoord, coordToPlot in enumerate(coordsToPlot):
            coord = torques_opencap.getDependentColumn(f'{coordToPlot}_moment').to_numpy() / mass
            time_interp = np.linspace(time[0], time[-1], N)
            joint_torques_opencap[trial][:, icoord, isubj] = np.interp(time_interp, time, coord)


# Plot addbio vs opencap joint angles mean +/- std across subjects
fig, axs = plt.subplots(3, 2, figsize=(4.5, 7))
for itrial, trial in enumerate(trials):
    pgc = np.linspace(0, 100, N)
    if trial == 'squats1':
        pgc = np.linspace(0, 100, Nsub)
        joint_angles_opencap[trial] = joint_angles_opencap[trial][:Nsub, :, :]
        joint_angles_addbio[trial] = joint_angles_addbio[trial][:Nsub, :, :]

    for icoord, coordToPlot in enumerate(coordsToPlot):
        axs[icoord, itrial].plot(pgc, np.mean(joint_angles_opencap[trial][:, icoord, :], axis=1),
                                 color=color_opencap, linewidth=2.5)
        axs[icoord, itrial].plot(pgc, np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1),
                                 color=color_addbio, linewidth=2.5)
        axs[icoord, itrial].fill_between(pgc,
                                         np.mean(joint_angles_opencap[trial][:, icoord, :], axis=1) - np.std(joint_angles_opencap[trial][:, icoord, :], axis=1),
                                         np.mean(joint_angles_opencap[trial][:, icoord, :], axis=1) + np.std(joint_angles_opencap[trial][:, icoord, :], axis=1),
                                         color=color_opencap, alpha=0.2, edgecolor='none')
        axs[icoord, itrial].fill_between(pgc,
                                         np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1) - np.std(joint_angles_addbio[trial][:, icoord, :], axis=1),
                                         np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1) + np.std(joint_angles_addbio[trial][:, icoord, :], axis=1),
                                         color=color_addbio, alpha=0.2, edgecolor='none')

        axs[icoord, itrial].set_xlim([0, 100])
        axs[icoord, itrial].set_xticks([0, 50, 100])
        if icoord == 0:
            axs[icoord, itrial].set_title(trial_names[itrial], fontsize=12)

        if icoord == 2:
            if trial == 'DJ':
                axs[icoord, itrial].set_xlabel('time (% drop jump)')
            elif trial == 'squats1':
                axs[icoord, itrial].set_xlabel('time (% squats)')

            axs[icoord, itrial].set_xticklabels([0, 50, 100])
        else:
            axs[icoord, itrial].set_xticklabels([])

        if icoord == 0:
            axs[icoord, itrial].set_ylim([-30, 120])
            axs[icoord, itrial].set_yticks([-30, 0, 30, 60, 90, 120])
            axs[icoord, itrial].set_yticklabels([-30, 0, 30, 60, 90, 120])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'hip flexion angle $[^\circ]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        elif icoord == 1:
            axs[icoord, itrial].set_ylim([0, 125])
            axs[icoord, itrial].set_yticks([0, 25, 50, 75, 100, 125])
            axs[icoord, itrial].set_yticklabels([0, 25, 50, 75, 100, 125])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'knee angle $[^\circ]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        elif icoord == 2:
            axs[icoord, itrial].set_ylim([-40, 40])
            axs[icoord, itrial].set_yticks([-40, -20, 0, 20, 40])
            axs[icoord, itrial].set_yticklabels([-40, -20, 0, 20, 40])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'ankle angle $[^\circ]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        # axs[icoord, itrial].grid()
        axs[icoord, itrial].spines['top'].set_visible(False)
        axs[icoord, itrial].spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(os.path.join('figures', 'joint_angles_addbio_vs_opencap.png'), dpi=300, bbox_inches='tight')

# Plot addbio vs opencap joint torques mean +/- std across subjects
fig, axs = plt.subplots(3, 2, figsize=(4.5, 7))
for itrial, trial in enumerate(trials):
    pgc = np.linspace(0, 100, N)
    if trial == 'squats1':
        pgc = np.linspace(0, 100, Nsub)
        joint_torques_opencap[trial] = joint_torques_opencap[trial][:Nsub, :]
        joint_torques_addbio[trial] = joint_torques_addbio[trial][:Nsub, :]

    for icoord, coordToPlot in enumerate(coordsToPlot):
        axs[icoord, itrial].plot(pgc, np.mean(joint_torques_opencap[trial][:, icoord, :], axis=1),
                                 color=color_opencap, linewidth=2.5)
        axs[icoord, itrial].plot(pgc, np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1),
                                 color=color_addbio, linewidth=2.5)
        axs[icoord, itrial].fill_between(pgc,
                                         np.mean(joint_torques_opencap[trial][:, icoord, :], axis=1) - np.std(joint_torques_opencap[trial][:, icoord, :], axis=1),
                                         np.mean(joint_torques_opencap[trial][:, icoord, :], axis=1) + np.std(joint_torques_opencap[trial][:, icoord, :], axis=1),
                                         color=color_opencap, alpha=0.2, edgecolor='none')
        axs[icoord, itrial].fill_between(pgc,
                                         np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1) - np.std(joint_torques_addbio[trial][:, icoord, :], axis=1),
                                         np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1) + np.std(joint_torques_addbio[trial][:, icoord, :], axis=1),
                                         color=color_addbio, alpha=0.2, edgecolor='none')

        axs[icoord, itrial].set_xlim([0, 100])
        axs[icoord, itrial].set_xticks([0, 50, 100])
        if icoord == 0:
            axs[icoord, itrial].set_title(trial_names[itrial], fontsize=12)

        if icoord == 2:
            if trial == 'DJ':
                axs[icoord, itrial].set_xlabel('time (% drop jump)')
            elif trial == 'squats1':
                axs[icoord, itrial].set_xlabel('time (% squats)')
            axs[icoord, itrial].set_xticklabels([0, 50, 100])
        else:
            axs[icoord, itrial].set_xticklabels([])


        if icoord == 0:
            axs[icoord, itrial].set_ylim([-3, 3])
            axs[icoord, itrial].set_yticks([-3, -2, -1, 0, 1, 2, 3])
            axs[icoord, itrial].set_yticklabels([-3, -2, -1, 0, 1, 2, 3])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'hip flexion moment $[N \cdot m / kg]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        elif icoord == 1:
            axs[icoord, itrial].set_ylim([-3, 3])
            axs[icoord, itrial].set_yticks([-3, -2, -1, 0, 1, 2, 3])
            axs[icoord, itrial].set_yticklabels([-3, -2, -1, 0, 1, 2, 3])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'knee moment $[N \cdot m / kg]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        elif icoord == 2:
            axs[icoord, itrial].set_ylim([-2, 1])
            axs[icoord, itrial].set_yticks([-2, -1, 0, 1])
            axs[icoord, itrial].set_yticklabels([-2, -1, 0, 1])
            if itrial == 0:
                axs[icoord, itrial].set_ylabel(r'ankle moment $[N \cdot m / kg]$')
            else:
                axs[icoord, itrial].set_yticklabels([])

        # axs[icoord, itrial].grid()
        axs[icoord, itrial].spines['top'].set_visible(False)
        axs[icoord, itrial].spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(os.path.join('figures', 'joint_torques_addbio_vs_opencap.png'), dpi=300, bbox_inches='tight')