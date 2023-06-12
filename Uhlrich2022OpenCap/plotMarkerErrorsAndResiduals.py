import pandas as pd
import numpy as np
import os
import opensim as osim
import matplotlib.pyplot as plt
from plotting import storage2pandas
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

rad2deg = 180 / 3.14159
marker_rmse_addbio = np.zeros(len(subjects))
marker_rmse_opencap = np.zeros(len(subjects))
for isubj, subject in enumerate(subjects):

    # Marker errors (OpenCap)
    # ----------------------
    marker_rmse_rra_df = pd.read_csv('marker_rmse_opencap.csv')
    marker_rmse_rra_df = marker_rmse_rra_df.set_index('Subject')
    marker_rmse_opencap[isubj] = 100.0*marker_rmse_rra_df.loc[subject, 'Marker RMSE (m)']

    # Marker errors (AddBiomechanics)
    # -------------------------------
    results_fpath = os.path.join('Processed', subject, '_results.json')
    f = open(results_fpath)
    results = json.load(f)
    marker_rmse_addbio[isubj] = 100.0 * results['autoAvgRMSE']


# Create a figure with four subplots.
fig = plt.figure(figsize=(6, 4))
gs = fig.add_gridspec(1, 10, left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2)
axes = list()
axes.append(fig.add_subplot(gs[0, 0:3]))
axes.append(fig.add_subplot(gs[0, 4:10]))

# Plot settings.
ylabel_fs = 8
xlabel_fs = 9
yticklabel_fs = 7
colors_fpath = os.path.join('..', 'colors.json')
f = open(colors_fpath)
colors = json.load(f)
color_opencap = colors['original']
color_addbio = colors['addbio']
width = 0.3

# Plot the marker RMSE.
axes[0].bar(0 - 0.5*width, np.mean(marker_rmse_opencap), width, color=color_opencap)
axes[0].bar(0 + 0.5*width, np.mean(marker_rmse_addbio), width, color=color_addbio)
plot_errorbar(axes[0], 0 - 0.5*width, np.mean(marker_rmse_opencap), np.std(marker_rmse_opencap))
plot_errorbar(axes[0], 0 + 0.5*width, np.mean(marker_rmse_addbio), np.std(marker_rmse_addbio))
axes[0].set_ylabel(r'Average RMS Error $[cm]$', fontsize=ylabel_fs)
axes[0].set_xticks([0])
axes[0].set_xticklabels(['Marker Error'], fontsize=xlabel_fs)
axes[0].set_ylim([0, 5])
axes[0].set_yticks([0, 1, 2, 3, 4, 5])
axes[0].set_yticklabels([0, 1, 2, 3, 4, 5], fontsize=yticklabel_fs)
axes[0].set_xlim([-0.5, 0.5])

# Plot the residuals
residuals_addbio_df = pd.read_csv('residuals_addbio.csv')
mean_rms_forces_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_forces'].mean()
mean_rms_moments_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_moments'].mean()
std_rms_forces_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_forces'].std()
std_rms_moments_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_moments'].std()

residuals_opencap_df = pd.read_csv('residuals_opencap.csv')
mean_rms_forces_opencap = 100.0*residuals_opencap_df['kinetic_normalized_rms_forces'].mean()
mean_rms_moments_opencap = 100.0*residuals_opencap_df['kinetic_normalized_rms_moments'].mean()
std_rms_forces_opencap = 100.0*residuals_opencap_df['kinetic_normalized_rms_forces'].std()
std_rms_moments_opencap = 100.0*residuals_opencap_df['kinetic_normalized_rms_moments'].std()

axes[1].bar(0 - 0.5*width, mean_rms_forces_opencap, width, color=color_opencap)
axes[1].bar(0 + 0.5*width, mean_rms_forces_addbio, width, color=color_addbio)
h_opencap = axes[1].bar(0.75 - 0.5*width, mean_rms_moments_opencap, width, color=color_opencap)
h_addbio = axes[1].bar(0.75 + 0.5*width, mean_rms_moments_addbio, width, color=color_addbio)
plot_errorbar(axes[1], 0 - 0.5*width, mean_rms_forces_opencap, std_rms_forces_opencap)
plot_errorbar(axes[1], 0 + 0.5*width, mean_rms_forces_addbio, std_rms_forces_addbio)
plot_errorbar(axes[1], 0.75 - 0.5*width, mean_rms_moments_opencap, std_rms_moments_opencap)
plot_errorbar(axes[1], 0.75 + 0.5*width, mean_rms_moments_addbio, std_rms_moments_addbio)
axes[1].set_ylabel(r'Normalized Average RMS Residual Load $[\%]$', fontsize=ylabel_fs)
axes[1].set_xticks([0, 0.75])
axes[1].set_xticklabels(['Residual\nForce', 'Residual\nTorque'], fontsize=xlabel_fs)
axes[1].set_ylim([0, 25.0])
axes[1].set_yticks([0, 5, 10, 15, 20, 25])
axes[1].set_yticklabels([0, 5, 10, 15, 20, 25], fontsize=yticklabel_fs)
axes[1].set_xlim([-0.5, 1.25])
axes[1].axhline(5, color='black', linewidth=0.75, linestyle='--', alpha=0.5, xmin=0, xmax=0.5, clip_on=False)
h_hicks = axes[1].axhline(1, color='black', linewidth=0.75, linestyle='--', alpha=0.5, xmin=0.5, xmax=1.0,
                          clip_on=False)
legend = axes[1].legend([h_opencap, h_addbio, h_hicks],
                        ['Uhlrich et al. (2022)', 'AddBiomechanics', 'Thresholds suggested by\nHicks et al. (2015)'],
                        loc='upper right', fontsize=7, frameon=False)
labels = legend.get_texts()
labels[2].set_fontsize(6)
labels[2].set_alpha(0.75)

# Remove top and right spines.
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Save figure.
# fig.tight_layout()
fig.savefig(os.path.join('figures', 'markers_residuals_addbio_vs_opencap.png'), dpi=500, bbox_inches='tight')

# Print the mean and standard deviation of the residuals.
print('Uhlrich et al. (2022) residuals:')
print('  Forces:  %.2f +/- %.2f %%' % (mean_rms_forces_opencap, std_rms_forces_opencap))
print('  Moments: %.2f +/- %.2f %%' % (mean_rms_moments_opencap, std_rms_moments_opencap))

print('AddBiomechanics residuals:')
print('  Forces:  %.2f +/- %.2f %%' % (mean_rms_forces_addbio, std_rms_forces_addbio))
print('  Moments: %.2f +/- %.2f %%' % (mean_rms_moments_addbio, std_rms_moments_addbio))

# Print the mean and standard deviation of the marker errors.
print('Uhlrich et al. (2022) marker errors:')
print('  Average:  %.2f +/- %.2f mm' % (np.mean(marker_rmse_opencap), np.std(marker_rmse_opencap)))

print('AddBiomechanics marker errors:')
print('  Average:  %.2f +/- %.2f mm' % (np.mean(marker_rmse_addbio), np.std(marker_rmse_addbio)))