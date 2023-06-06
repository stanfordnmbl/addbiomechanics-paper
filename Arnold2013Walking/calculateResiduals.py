import os
import sys

import numpy as np
import pandas as pd
from residual_helpers import get_residuals, get_external_kinetics, compute_rmse

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
        residuals_by_trial = [trial for trial in residuals_by_trial if trial.startswith(subjectID+'_walk')
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
                                                    residual_force_names, residual_moment_names)

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
