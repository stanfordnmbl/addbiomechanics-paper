import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
dynfit_fpath = os.path.join('Processed')

rad2deg = 180 / 3.14159
marker_rmse_addbio = np.zeros(len(subjects))
marker_rmse_hamner = np.zeros(len(subjects))
for isubj, subject in enumerate(subjects):

    # Marker errors (Hamner)
    # ----------------------
    marker_rmse_rra_df = pd.read_csv('marker_rmse_rra.csv')
    marker_rmse_rra_df = marker_rmse_rra_df.set_index('Subject')
    marker_rmse_hamner[isubj] = 100.0*marker_rmse_rra_df.loc[subject, 'Marker RMSE (m)']

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
color_hamner = '#2e2e2e'
color_addbio = '#7798ce'
width = 0.3

# Plot the marker RMSE.
axes[0].bar(0 - 0.5*width, np.mean(marker_rmse_hamner), width, color=color_hamner)
axes[0].bar(0 + 0.5*width, np.mean(marker_rmse_addbio), width, color=color_addbio)
plot_errorbar(axes[0], 0 - 0.5*width, np.mean(marker_rmse_hamner), np.std(marker_rmse_hamner))
plot_errorbar(axes[0], 0 + 0.5*width, np.mean(marker_rmse_addbio), np.std(marker_rmse_addbio))
axes[0].set_ylabel(r'Average RMS Error $[cm]$', fontsize=ylabel_fs)
axes[0].set_xticks([0])
axes[0].set_xticklabels(['Marker Error'], fontsize=xlabel_fs)
axes[0].set_ylim([0, 5])
axes[0].set_yticks([0, 1, 2, 3, 4, 5])
axes[0].set_yticklabels([0, 1, 2, 3, 4, 5], fontsize=yticklabel_fs)
axes[0].set_xlim([-0.5, 0.5])

# Plot the residuals
residuals_addbio_df = pd.read_csv('residuals_summary_addbio.csv')
mean_rms_forces_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_forces'].mean()
mean_rms_moments_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_moments'].mean()
std_rms_forces_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_forces'].std()
std_rms_moments_addbio = 100.0*residuals_addbio_df['kinetic_normalized_rms_moments'].std()

residuals_hamner_df = pd.read_csv('residuals_summary_hamner.csv')
mean_rms_forces_hamner = 100.0*residuals_hamner_df['kinetic_normalized_rms_forces'].mean()
mean_rms_moments_hamner = 100.0*residuals_hamner_df['kinetic_normalized_rms_moments'].mean()
std_rms_forces_hamner = 100.0*residuals_hamner_df['kinetic_normalized_rms_forces'].std()
std_rms_moments_hamner = 100.0*residuals_hamner_df['kinetic_normalized_rms_moments'].std()

axes[1].bar(0 - 0.5*width, mean_rms_forces_hamner, width, color=color_hamner)
axes[1].bar(0 + 0.5*width, mean_rms_forces_addbio, width, color=color_addbio)
h_hamner = axes[1].bar(0.75 - 0.5*width, mean_rms_moments_hamner, width, color=color_hamner)
h_addbio = axes[1].bar(0.75 + 0.5*width, mean_rms_moments_addbio, width, color=color_addbio)
plot_errorbar(axes[1], 0 - 0.5*width, mean_rms_forces_hamner, std_rms_forces_hamner)
plot_errorbar(axes[1], 0 + 0.5*width, mean_rms_forces_addbio, std_rms_forces_addbio)
plot_errorbar(axes[1], 0.75 - 0.5*width, mean_rms_moments_hamner, std_rms_moments_hamner)
plot_errorbar(axes[1], 0.75 + 0.5*width, mean_rms_moments_addbio, std_rms_moments_addbio)
axes[1].set_ylabel(r'Normalized Average RMS Residual Load $[\%]$', fontsize=ylabel_fs)
axes[1].set_xticks([0, 0.75])
axes[1].set_xticklabels(['Residual\nForce', 'Residual\nTorque'], fontsize=xlabel_fs)
axes[1].set_ylim([0, 5.0])
axes[1].set_yticks([0, 1, 2, 3, 4, 5])
axes[1].set_yticklabels([0, 1, 2, 3, 4, 5], fontsize=yticklabel_fs)
# axes[1].set_ylim([0, 25.0])
# axes[1].set_yticks([0, 5, 10, 15, 20, 25])
# axes[1].set_yticklabels([0, 5, 10, 15, 20, 25], fontsize=yticklabel_fs)
axes[1].set_xlim([-0.5, 1.25])
axes[1].axhline(5, color='black', linewidth=0.75, linestyle='--', alpha=0.5, xmin=0, xmax=0.5, clip_on=False)
h_hicks = axes[1].axhline(1, color='black', linewidth=0.75, linestyle='--', alpha=0.5, xmin=0.5, xmax=1.0,
                          clip_on=False)
legend = axes[1].legend([h_hamner, h_addbio, h_hicks],
                        ['Hamner et al. (2013)', 'AddBiomechanics', 'Thresholds suggested by\nHicks et al. (2015)'],
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
fig.savefig(os.path.join('figures', 'markers_residuals_addbio_vs_hamner.png'), dpi=500, bbox_inches='tight')

# Print the mean and standard deviation of the residuals.
print('Hamner et al. (2013) residuals:')
print('  Forces:  %.2f +/- %.2f %%' % (mean_rms_forces_hamner, std_rms_forces_hamner))
print('  Moments: %.2f +/- %.2f %%' % (mean_rms_moments_hamner, std_rms_moments_hamner))

print('AddBiomechanics residuals:')
print('  Forces:  %.2f +/- %.2f %%' % (mean_rms_forces_addbio, std_rms_forces_addbio))
print('  Moments: %.2f +/- %.2f %%' % (mean_rms_moments_addbio, std_rms_moments_addbio))

# Print the mean and standard deviation of the marker errors.
print('Hamner et al. (2013) marker errors:')
print('  Average:  %.2f +/- %.2f mm' % (np.mean(marker_rmse_hamner), np.std(marker_rmse_hamner)))

print('AddBiomechanics marker errors:')
print('  Average:  %.2f +/- %.2f mm' % (np.mean(marker_rmse_addbio), np.std(marker_rmse_addbio)))
