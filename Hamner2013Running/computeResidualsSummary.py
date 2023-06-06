import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def computeMassNormalizedResiduals(post_rra_df, addbio_df):
    mean_rms_forces_rra = post_rra_df['mass_normalized_rms_forces'].mean()
    mean_rms_moments_rra = post_rra_df['mass_normalized_rms_moments'].mean()
    mean_rms_forces_addbio = addbio_df['mass_normalized_rms_forces'].mean()
    mean_rms_moments_addbio = addbio_df['mass_normalized_rms_moments'].mean()

    percent_diff_forces = 100.0 * (mean_rms_forces_rra - mean_rms_forces_addbio) / mean_rms_forces_rra
    percent_diff_moments = 100.0 * (mean_rms_moments_rra - mean_rms_moments_addbio) / mean_rms_moments_rra
    print('Percent difference in average RMS forces: {0:.2f}%'.format(percent_diff_forces))
    print('Percent difference in average RMS moments: {0:.2f}%'.format(percent_diff_moments))

    print('Average RMS forces RRA: {0:.2f} N/kg'.format(mean_rms_forces_rra))
    print('Average RMS moments RRA: {0:.2f} N-m/kg'.format(mean_rms_moments_rra))
    print('Average RMS forces AddBio: {0:.2f} N/kg'.format(mean_rms_forces_addbio))
    print('Average RMS moments AddBio: {0:.2f} N-m/kg'.format(mean_rms_moments_addbio))

def computeRawResiduals(post_rra_df, addbio_df):

    forces_rra = post_rra_df['raw_rms_forces'].mean()
    moments_rra = post_rra_df['raw_rms_moments'].mean()
    forces_addbio = addbio_df['raw_rms_forces'].mean()
    moments_addbio = addbio_df['raw_rms_moments'].mean()

    percent_diff_forces = 100.0 * (forces_rra - forces_addbio) / forces_rra
    percent_diff_moments = 100.0 * (moments_rra - moments_addbio) / moments_rra
    print('Percent difference in average RMS forces: {0:.2f}%'.format(percent_diff_forces))
    print('Percent difference in average RMS moments: {0:.2f}%'.format(percent_diff_moments))

    print('Average RMS forces RRA: {0:.2f} N'.format(forces_rra))
    print('Average RMS moments RRA: {0:.2f} N-m'.format(moments_rra))
    print('Average RMS forces AddBio: {0:.2f} N'.format(forces_addbio))
    print('Average RMS moments AddBio: {0:.2f} N-m'.format(moments_addbio))


addbio_df = pd.read_csv('residuals_summary_addbio.csv')
post_rra_df = pd.read_csv('residuals_summary_hamner.csv')
computeMassNormalizedResiduals(post_rra_df, addbio_df)
computeRawResiduals(post_rra_df, addbio_df)





