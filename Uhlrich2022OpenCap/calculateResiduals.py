import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from numpy.linalg import norm

from plotting import storage2pandas

def get_residuals(filename, residual_force_names, residual_moment_names, source):
    # extract residuals for the given trial.
    #
    # Args:
    #   filename (str): .sto file containing residual waveforms.
    #
    # Returns:
    #   res_forces (array): vector of residual force magnitude over the
    #                       trial.
    #   res_moms (array): vector of residual moment magnitude over the
    #                     trial.

    header_shift = -1 if source == 'addbio' else 1
    residuals = storage2pandas(filename, header_shift=header_shift)
    residuals_forces = residuals[residual_force_names].to_numpy()
    residuals_moments = residuals[residual_moment_names].to_numpy()

    res_forces = norm(residuals_forces, axis=1)
    res_moms = norm(residuals_moments, axis=1)

    # resample to 101 points
    res_forces = interp1d(np.arange(len(res_forces)), res_forces, kind='linear')(
        np.linspace(0, len(res_forces) - 1, 101))
    res_moms = interp1d(np.arange(len(res_moms)), res_moms, kind='linear')(np.linspace(0, len(res_moms) - 1, 101))

    return res_forces, res_moms


def get_external_kinetics(com_filename, grf_filename, source):
    # get maximum external force and maximum external force * center of
    # mass height values across the trial.
    #
    # Args:
    #   com_filename (str): .sto file containing COM waveforms.
    #   grf_filename (str): .mot file containing filtered GRF waveforms.
    #
    # Returns:
    #   max_ext_force (float): maximum external force magnitude.
    #   max_ext_mom (float): maximum value of external force magnitude *
    #                        mean center of mass height.
    #
    # Notes:
    #   ext_moms aren't exactly external moments. They are COM height *
    #   external force magnitude.

    # load COM data
    positions = storage2pandas(com_filename, header_shift=-4)
    times = positions['time'].values
    start = times[0]
    stop = times[-1]
    com_heights = positions['center_of_mass_Y'].values
    # resample to 101 points
    mean_com_height = np.mean(com_heights)

    # load GRF data
    header_shift = 0 if source == 'addbio' else 1
    grf = storage2pandas(grf_filename, header_shift=header_shift)
    times = grf['time'].values
    if 'addbio' in source:
        forces_1 = grf[['ground_force_calcn_r_vx', 'ground_force_calcn_r_vy', 'ground_force_calcn_r_vz']].values
        forces_2 = grf[['ground_force_calcn_l_vx', 'ground_force_calcn_l_vy', 'ground_force_calcn_l_vz']].values
    elif 'opencap' in source:
        forces_1 = grf[['R_ground_force_vx', 'R_ground_force_vy', 'R_ground_force_vz']].values
        forces_2 = grf[['L_ground_force_vx', 'L_ground_force_vy', 'L_ground_force_vz']].values

    forces = forces_1 + forces_2

    # keep only relevant times and resample to 101 points
    interp_times = np.linspace(start, stop, 101)
    interp_func = interp1d(times, forces, axis=0)
    forces = interp_func(interp_times)

    ext_forces = np.linalg.norm(forces, axis=1)

    max_ext_force = np.max(ext_forces)
    max_ext_mom = mean_com_height * max_ext_force
    # note not exactly external moment; magnitude of force * COM height

    return max_ext_force, max_ext_mom


def compute_rmse(yhat, y):
    """
    Compute the root-mean-square error.

    Args:
    yhat (array): estimates.
    y (array): observations.

    Returns:
    rmse (float): root-mean-square error.
    """
    rmse = np.sqrt(np.mean((y - yhat) ** 2))
    return rmse

def calculateResiduals(argv):
    source = argv[1]
    waveforms_filepath = os.path.join('residuals', source)

    residual_force_names = ['pelvis_tx_force', 'pelvis_ty_force', 'pelvis_tz_force']
    residual_moment_names = ['pelvis_list_moment', 'pelvis_rotation_moment', 'pelvis_tilt_moment']

    # read subject list
    demographics = pd.read_csv('demographics.csv')
    subjectIDs = demographics['subject']
    subject_masses = demographics['weight (kg)']

    n_subjects = len(subjectIDs)
    raw_peak_forces = np.zeros(n_subjects)
    raw_rms_forces = np.zeros(n_subjects)
    raw_peak_moments = np.zeros(n_subjects)
    raw_rms_moments = np.zeros(n_subjects)
    mass_normalized_peak_forces = np.zeros(n_subjects)
    mass_normalized_rms_forces = np.zeros(n_subjects)
    mass_normalized_peak_moments = np.zeros(n_subjects)
    mass_normalized_rms_moments = np.zeros(n_subjects)
    kinetic_normalized_peak_forces = np.zeros(n_subjects)
    kinetic_normalized_rms_forces = np.zeros(n_subjects)
    kinetic_normalized_peak_moments = np.zeros(n_subjects)
    kinetic_normalized_rms_moments = np.zeros(n_subjects)

    for i in range(n_subjects):
        subjectID = str(subjectIDs[i])
        subject_mass = subject_masses[i] # kg

        # trial filenames associated with this subjectID
        residuals_by_trial = os.listdir(waveforms_filepath)
        residuals_by_trial = [trial for trial in residuals_by_trial if trial.startswith(subjectID)
                                                                    and trial.endswith('_residuals.sto')]
        n_trials = len(residuals_by_trial)

        subject_raw_peak_forces = np.zeros(n_trials)
        subject_raw_rms_forces = np.zeros(n_trials)
        subject_raw_peak_moments = np.zeros(n_trials)
        subject_raw_rms_moments = np.zeros(n_trials)

        subject_mass_normalized_peak_forces = np.zeros(n_trials)
        subject_mass_normalized_rms_forces = np.zeros(n_trials)
        subject_mass_normalized_peak_moments = np.zeros(n_trials)
        subject_mass_normalized_rms_moments = np.zeros(n_trials)

        subject_kinetic_normalized_peak_forces = np.zeros(n_trials)
        subject_kinetic_normalized_rms_forces = np.zeros(n_trials)
        subject_kinetic_normalized_peak_moments = np.zeros(n_trials)
        subject_kinetic_normalized_rms_moments = np.zeros(n_trials)

        # loop over trials for subject
        for j in range(n_trials):
            # read waveform data
            filename = residuals_by_trial[j]
            res_forces, res_moments = get_residuals(os.path.join(waveforms_filepath, filename),
                                                    residual_force_names, residual_moment_names, source)

            subject_raw_peak_forces[j] = np.max(res_forces)
            subject_raw_rms_forces[j] = compute_rmse(res_forces, 0)
            subject_raw_peak_moments[j] = np.max(res_moments)
            subject_raw_rms_moments[j] = compute_rmse(res_moments, 0)

            # get normalized peak and rms residuals and append to subject data
            mass_normalized_res_forces = res_forces / subject_mass
            mass_normalized_res_moments = res_moments / subject_mass

            subject_mass_normalized_peak_forces[j] = np.max(mass_normalized_res_forces)
            subject_mass_normalized_rms_forces[j] = compute_rmse(mass_normalized_res_forces, 0)
            subject_mass_normalized_peak_moments[j] = np.max(mass_normalized_res_moments)
            subject_mass_normalized_rms_moments[j] = compute_rmse(mass_normalized_res_moments, 0)

            # Get peak and RMS residuals as percentages of net external force and COM height
            com_filename = os.path.join(waveforms_filepath, filename[:-13] + 'com.sto')
            grf_filename = os.path.join(waveforms_filepath, filename[:-13] + 'grf.mot')
            max_ext_force, max_ext_moment = get_external_kinetics(com_filename, grf_filename, source)

            kinetic_normalized_res_forces = res_forces.reshape((1, 101)) / max_ext_force
            kinetic_normalized_res_moments = res_moments.reshape((1, 101)) / max_ext_moment

            subject_kinetic_normalized_peak_forces[j] = np.max(kinetic_normalized_res_forces)
            subject_kinetic_normalized_rms_forces[j] = compute_rmse(kinetic_normalized_res_forces, 0)
            subject_kinetic_normalized_peak_moments[j] = np.max(kinetic_normalized_res_moments)
            subject_kinetic_normalized_rms_moments[j] = compute_rmse(kinetic_normalized_res_moments, 0)

        # Append trial averages
        raw_peak_forces[i] = np.mean(subject_raw_peak_forces)
        raw_rms_forces[i] = np.mean(subject_raw_rms_forces)
        raw_peak_moments[i] = np.mean(subject_raw_peak_moments)
        raw_rms_moments[i] = np.mean(subject_raw_rms_moments)

        mass_normalized_peak_forces[i] = np.mean(subject_mass_normalized_peak_forces)
        mass_normalized_rms_forces[i] = np.mean(subject_mass_normalized_rms_forces)
        mass_normalized_peak_moments[i] = np.mean(subject_mass_normalized_peak_moments)
        mass_normalized_rms_moments[i] = np.mean(subject_mass_normalized_rms_moments)

        kinetic_normalized_peak_forces[i] = np.mean(subject_kinetic_normalized_peak_forces)
        kinetic_normalized_rms_forces[i] = np.mean(subject_kinetic_normalized_rms_forces)
        kinetic_normalized_peak_moments[i] = np.mean(subject_kinetic_normalized_peak_moments)
        kinetic_normalized_rms_moments[i] = np.mean(subject_kinetic_normalized_rms_moments)

    # Save data to a CSV file
    data = np.vstack((subjectIDs, raw_peak_forces, raw_rms_forces, raw_peak_moments, raw_rms_moments,
                      mass_normalized_peak_forces, mass_normalized_rms_forces, mass_normalized_peak_moments,
                      mass_normalized_rms_moments, kinetic_normalized_peak_forces, kinetic_normalized_rms_forces,
                      kinetic_normalized_peak_moments, kinetic_normalized_rms_moments)).T
    df = pd.DataFrame(data, columns=['subjectID', 'raw_peak_forces', 'raw_rms_forces', 'raw_peak_moments',
                                     'raw_rms_moments', 'mass_normalized_peak_forces', 'mass_normalized_rms_forces',
                                     'mass_normalized_peak_moments', 'mass_normalized_rms_moments',
                                     'kinetic_normalized_peak_forces', 'kinetic_normalized_rms_forces',
                                     'kinetic_normalized_peak_moments', 'kinetic_normalized_rms_moments'])
    df.to_csv(f'residuals_{source}.csv', index=False)


if __name__ == '__main__':
    calculateResiduals(sys.argv)
