import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import storage2pandas
import json
from dictionaries import trial_dict, subject_dict, init_cycle_dict, second_cycle_dict, final_cycle_dict

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['mathtext.rm'] = 'serif'

colors_fpath = os.path.join('..', 'colors.json')
f = open(colors_fpath)
colors = json.load(f)
color_hamner = colors['original']
color_addbio = colors['addbio']

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']
dynfit_fpath = os.path.join('Processed')
hamner_fpath = os.path.join('residuals', 'hamner')
addbio_fpath = os.path.join('residuals', 'addbio')

rad2deg = 180 / 3.14159
marker_rmse_addbio = np.zeros(len(subjects))
marker_rmse_hamner = np.zeros(len(subjects))
trials = ['run200', 'run500']
trial_names = ['2.0 m/s', '5.0 m/s']
coordsToPlot = ['hip_flexion_r', 'knee_angle_r', 'ankle_angle_r']
joint_angles_hamner = dict()
joint_angles_addbio = dict()
joint_torques_hamner = dict()
joint_torques_addbio = dict()
for trial in trials:
    joint_angles_hamner[trial] = np.zeros((101, len(coordsToPlot), len(subjects)))
    joint_angles_addbio[trial] = np.zeros((101, len(coordsToPlot), len(subjects)))
    joint_torques_hamner[trial] = np.zeros((101, len(coordsToPlot), len(subjects)))
    joint_torques_addbio[trial] = np.zeros((101, len(coordsToPlot), len(subjects)))

for isubj, (subject, mass) in enumerate(zip(subjects, masses)):

    # Loop over all trials for this subject
    for itrial, trial in enumerate(trials):

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
        joint_angles_hamner_cycles = np.zeros((101, len(coordsToPlot), 3))
        joint_angles_addbio_cycles = np.zeros((101, len(coordsToPlot), 3))
        joint_torques_hamner_cycles = np.zeros((101, len(coordsToPlot), 3))
        joint_torques_addbio_cycles = np.zeros((101, len(coordsToPlot), 3))
        for icycle, (cycle, cycle_dict) in enumerate(zip(cycles, cycle_dicts)):
            # update cycle number, if needed
            if subject in cycle_dict.keys():
                for cycle_tuple in cycle_dict[subject]:
                    if cycle_tuple[0] == trial:
                        cycle = cycle_tuple[1]

            # Joint angles (Hamner)
            # ---------------------
            coordinates_hamner_fpath = os.path.join(hamner_fpath, 'results', subject, 'trials', trial,
                                             f'{subject}_{trial}_cycle{cycle}_coordinates.sto')
            coordinates_hamner = osim.TimeSeriesTable(coordinates_hamner_fpath)
            time = np.array(coordinates_hamner.getIndependentColumn())
            for icoord, coordToPlot in enumerate(coordsToPlot):
                sign = -1 if 'knee' in coordToPlot else 1
                coord = sign*coordinates_hamner.getDependentColumn(coordToPlot).to_numpy()
                time_interp = np.linspace(time[0], time[-1], 101)
                joint_angles_hamner_cycles[:, icoord, icycle] = np.interp(time_interp, time, coord)

            # Joint angles (AddBiomechanics)
            # ------------------------------
            coordinates_addbio_fpath = os.path.join(dynfit_fpath, subject, 'osim_results', 'IK', f'{trial}_ik.mot')
            coordinates_addbio = osim.TimeSeriesTable(coordinates_addbio_fpath)
            coordinates_addbio.trim(time[0], time[-1])
            time = np.array(coordinates_addbio.getIndependentColumn())
            for icoord, coordToPlot in enumerate(coordsToPlot):
                sign = -1 if 'knee' in coordToPlot else 1
                coord = sign*rad2deg*coordinates_addbio.getDependentColumn(coordToPlot).to_numpy()
                time_interp = np.linspace(time[0], time[-1], 101)
                joint_angles_addbio_cycles[:, icoord, icycle] = np.interp(time_interp, time, coord)

            # Joint torques (Hamner)
            # ----------------------
            torques_hamner_fpath = os.path.join(hamner_fpath, f'{subject}_{trial}_cycle{cycle}_residuals.sto')
            torques_hamner = osim.TimeSeriesTable(torques_hamner_fpath)
            time = np.array(torques_hamner.getIndependentColumn())
            for icoord, coordToPlot in enumerate(coordsToPlot):
                sign = -1 if 'knee' in coordToPlot else 1
                coord = sign*torques_hamner.getDependentColumn(coordToPlot).to_numpy() / mass
                time_interp = np.linspace(time[0], time[-1], 101)
                joint_torques_hamner_cycles[:, icoord, icycle] = np.interp(time_interp, time, coord)

            # Joint torques (AddBiomechanics)
            # -------------------------------
            torques_addbio_fpath = os.path.join(addbio_fpath, f'{subject}_{trial}_cycle{cycle}_residuals.sto')
            torques_addbio = osim.TimeSeriesTable(torques_addbio_fpath)
            torques_addbio.trim(time[0], time[-1])
            time = np.array(torques_addbio.getIndependentColumn())
            for icoord, coordToPlot in enumerate(coordsToPlot):
                sign = -1 if 'knee' in coordToPlot else 1
                coord = sign*torques_addbio.getDependentColumn(f'{coordToPlot}_moment').to_numpy() / mass
                time_interp = np.linspace(time[0], time[-1], 101)
                joint_torques_addbio_cycles[:, icoord, icycle] = np.interp(time_interp, time, coord)

        joint_angles_hamner[trial][:, :, isubj] = np.mean(joint_angles_hamner_cycles, axis=2)
        joint_angles_addbio[trial][:, :, isubj] = np.mean(joint_angles_addbio_cycles, axis=2)
        joint_torques_hamner[trial][:, :, isubj] = np.mean(joint_torques_hamner_cycles, axis=2)
        joint_torques_addbio[trial][:, :, isubj] = np.mean(joint_torques_addbio_cycles, axis=2)

# Plot addbio vs hamner joint angles mean +/- std across subjects
fig, axs = plt.subplots(3, 2, figsize=(4.5, 7))
pgc = np.linspace(0, 100, 101)
for itrial, trial in enumerate(trials):
    for icoord, coordToPlot in enumerate(coordsToPlot):
        axs[icoord, itrial].plot(pgc, np.mean(joint_angles_hamner[trial][:, icoord, :], axis=1),
                                 color=color_hamner, linewidth=2.5)
        axs[icoord, itrial].plot(pgc, np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1),
                                 color=color_addbio, linewidth=2.5)
        axs[icoord, itrial].fill_between(pgc,
             np.mean(joint_angles_hamner[trial][:, icoord, :], axis=1) - np.std(joint_angles_hamner[trial][:, icoord, :], axis=1),
             np.mean(joint_angles_hamner[trial][:, icoord, :], axis=1) + np.std(joint_angles_hamner[trial][:, icoord, :], axis=1),
             color=color_hamner, alpha=0.2, edgecolor='none')
        axs[icoord, itrial].fill_between(pgc,
            np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1) - np.std(joint_angles_addbio[trial][:, icoord, :], axis=1),
            np.mean(joint_angles_addbio[trial][:, icoord, :], axis=1) + np.std(joint_angles_addbio[trial][:, icoord, :], axis=1),
            color=color_addbio, alpha=0.2, edgecolor='none')

        axs[icoord, itrial].set_xlim([0, 100])
        axs[icoord, itrial].set_xticks([0, 50, 100])
        if icoord == 0:
            axs[icoord, itrial].set_title(trial_names[itrial], fontsize=12)

        if icoord == 2:
            axs[icoord, itrial].set_xlabel('gait cycle (%)')
            axs[icoord, itrial].set_xticklabels([0, 50, 100])
        else:
            axs[icoord, itrial].set_xticklabels([])

        if itrial == 0:
            if icoord == 0:
                axs[icoord, itrial].set_ylim([-40, 80])
                axs[icoord, itrial].set_yticks([-40, -20, 0, 20, 40, 60, 80])
                axs[icoord, itrial].set_yticklabels([-40, -20, 0, 20, 40, 60, 80])
                axs[icoord, itrial].set_ylabel(r'hip flexion angle $[^\circ]$')

            elif icoord == 1:
                axs[icoord, itrial].set_ylim([0, 150])
                axs[icoord, itrial].set_yticks([0, 25, 50, 75, 100, 125, 150])
                axs[icoord, itrial].set_yticklabels([0, 25, 50, 75, 100, 125, 150])
                axs[icoord, itrial].set_ylabel(r'knee angle $[^\circ]$')

            elif icoord == 2:
                axs[icoord, itrial].set_ylim([-40, 40])
                axs[icoord, itrial].set_yticks([-40, -20, 0, 20, 40])
                axs[icoord, itrial].set_yticklabels([-40, -20, 0, 20, 40])
                axs[icoord, itrial].set_ylabel(r'ankle angle $[^\circ]$')
        else:
            if icoord == 0:
                axs[icoord, itrial].set_ylim([-40, 80])
                axs[icoord, itrial].set_yticks([-40, -20, 0, 20, 40, 60, 80])
            elif icoord == 1:
                axs[icoord, itrial].set_ylim([0, 150])
                axs[icoord, itrial].set_yticks([0, 25, 50, 75, 100, 125, 150])
            elif icoord == 2:
                axs[icoord, itrial].set_ylim([-40, 40])
                axs[icoord, itrial].set_yticks([-40, -20, 0, 20, 40])
            axs[icoord, itrial].set_yticklabels([])

        # axs[icoord, itrial].grid()
        axs[icoord, itrial].spines['top'].set_visible(False)
        axs[icoord, itrial].spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(os.path.join('figures', 'joint_angles_addbio_vs_hamner.png'), dpi=300, bbox_inches='tight')

# Plot addbio vs hamner joint torques mean +/- std across subjects
fig, axs = plt.subplots(3, 2, figsize=(4.5, 7))
pgc = np.linspace(0, 100, 101)
for itrial, trial in enumerate(trials):
    for icoord, coordToPlot in enumerate(coordsToPlot):
        axs[icoord, itrial].plot(pgc, np.mean(joint_torques_hamner[trial][:, icoord, :], axis=1),
                                 color=color_hamner, linewidth=2.5)
        axs[icoord, itrial].plot(pgc, np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1),
                                 color=color_addbio, linewidth=2.5)
        axs[icoord, itrial].fill_between(pgc,
             np.mean(joint_torques_hamner[trial][:, icoord, :], axis=1) - np.std(joint_torques_hamner[trial][:, icoord, :], axis=1),
             np.mean(joint_torques_hamner[trial][:, icoord, :], axis=1) + np.std(joint_torques_hamner[trial][:, icoord, :], axis=1),
             color=color_hamner, alpha=0.2, edgecolor='none')
        axs[icoord, itrial].fill_between(pgc,
            np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1) - np.std(joint_torques_addbio[trial][:, icoord, :], axis=1),
            np.mean(joint_torques_addbio[trial][:, icoord, :], axis=1) + np.std(joint_torques_addbio[trial][:, icoord, :], axis=1),
            color=color_addbio, alpha=0.2, edgecolor='none')

        axs[icoord, itrial].set_xlim([0, 100])
        axs[icoord, itrial].set_xticks([0, 50, 100])
        if icoord == 0:
            axs[icoord, itrial].set_title(trial_names[itrial], fontsize=12)

        if icoord == 2:
            axs[icoord, itrial].set_xlabel('gait cycle (%)')
            axs[icoord, itrial].set_xticklabels([0, 50, 100])
        else:
            axs[icoord, itrial].set_xticklabels([])


        if itrial == 0:
            if icoord == 0:
                axs[icoord, itrial].set_ylim([-4, 4])
                axs[icoord, itrial].set_yticks([-4, -2, 0, 2, 4])
                axs[icoord, itrial].set_yticklabels([-4, -2, 0, 2, 4])
                axs[icoord, itrial].set_ylabel(r'hip flexion moment $[N \cdot m / kg]$')

            elif icoord == 1:
                axs[icoord, itrial].set_ylim([-4, 4])
                axs[icoord, itrial].set_yticks([-4, -2, 0, 2, 4])
                axs[icoord, itrial].set_yticklabels([-4, -2, 0, 2, 4])
                axs[icoord, itrial].set_ylabel(r'knee moment $[N \cdot m / kg]$')

            elif icoord == 2:
                axs[icoord, itrial].set_ylim([-5, 1])
                axs[icoord, itrial].set_yticks([-5, -4, -3, -2, -1, 0, 1])
                axs[icoord, itrial].set_yticklabels([-5, -4, -3, -2, -1, 0, 1])
                axs[icoord, itrial].set_ylabel(r'ankle moment $[N \cdot m / kg]$')
        else:
            if icoord == 0:
                axs[icoord, itrial].set_ylim([-4, 4])
                axs[icoord, itrial].set_yticks([-4, -2, 0, 2, 4])
            elif icoord == 1:
                axs[icoord, itrial].set_ylim([-4, 4])
                axs[icoord, itrial].set_yticks([-4, -2, 0, 2, 4])
            elif icoord == 2:
                axs[icoord, itrial].set_ylim([-5, 1])
                axs[icoord, itrial].set_yticks([-5, -4, -3, -2, -1, 0, 1])
            axs[icoord, itrial].set_yticklabels([])

        # axs[icoord, itrial].grid()
        axs[icoord, itrial].spines['top'].set_visible(False)
        axs[icoord, itrial].spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(os.path.join('figures', 'joint_torques_addbio_vs_hamner.png'), dpi=300, bbox_inches='tight')