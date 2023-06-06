import sys
import pandas as pd
import os
import numpy as np
import json

def computeResultsAcrossSubjects(argv):
    # Load subject information
    demographics_df = pd.read_csv('demographics.csv')
    subjects = demographics_df['subject']

    # Residual forces
    marker_rmse = np.zeros(len(subjects))
    marker_max_error = np.zeros(len(subjects))
    for isubj, subject in enumerate(subjects):
        results_fpath = os.path.join('Processed', subject, '_results.json')
        f = open(results_fpath)
        results = json.load(f)

        marker_rmse[isubj] = results['autoAvgRMSE']
        marker_max_error[isubj] = results['autoAvgMax']

    # Print results
    print(f'Marker RMSE across subjects: {100 * np.mean(marker_rmse):1.3f} +/- {100 * np.std(marker_rmse):1.3f} cm')
    print(f'Marker max error across subjects: {100 * np.mean(marker_max_error):1.3f} +/- {100 * np.std(marker_max_error):1.3f} cm')

    # Compute residuals
    residual_force = np.zeros(len(subjects))
    residual_torque = np.zeros(len(subjects))
    for isubj, subject in enumerate(subjects):
        results_fpath = os.path.join('Processed', subject, '_results.json')
        f = open(results_fpath)
        results = json.load(f)

        residual_force[isubj] = results['linearResidual']
        residual_torque[isubj] = results['angularResidual']

    # Print results
    print(f'Residual forces across subjects: {np.mean(residual_force):1.2f} +/- {np.std(residual_force):1.2f} N')
    print(f'Residual torques across subjects: {np.mean(residual_torque):1.2f} +/- {np.std(residual_torque):1.2f} N-m')

    # Write to text file
    dest_fpath = os.path.join('Processed', 'results_summary.txt')
    with open(dest_fpath, 'w') as f:
        f.write(f'Marker RMSE across subjects: {100 * np.mean(marker_rmse):1.3f} +/- {100 * np.std(marker_rmse):1.3f} cm\n')
        f.write(f'Marker max error across subjects: {100 * np.mean(marker_max_error):1.3f} +/- {100 * np.std(marker_max_error):1.3f} cm\n')
        f.write(f'Residual forces across subjects: {np.mean(residual_force):1.2f} +/- {np.std(residual_force):1.2f} N\n')
        f.write(f'Residual torques across subjects: {np.mean(residual_torque):1.2f} +/- {np.std(residual_torque):1.2f} N-m\n')

if __name__ == "__main__":
    computeResultsAcrossSubjects(sys.argv)