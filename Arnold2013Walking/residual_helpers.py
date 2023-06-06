import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from numpy.linalg import norm
from plotting import storage2pandas


def get_residuals(filename, residual_force_names, residual_moment_names):
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

    residuals = storage2pandas(filename, header_shift=-1)
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
    forces = storage2pandas(grf_filename, header_shift=0)
    times = forces['time'].values
    forces_1 = forces[['ground_force_calcn_r_vx', 'ground_force_calcn_r_vy', 'ground_force_calcn_r_vz']].values
    forces_2 = forces[['ground_force_calcn_l_vx', 'ground_force_calcn_l_vy', 'ground_force_calcn_l_vz']].values
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
