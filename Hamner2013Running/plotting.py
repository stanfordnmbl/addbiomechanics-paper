import os
import numpy as np
from collections import defaultdict, OrderedDict
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.lines as mlines

# Convert a STO file to a pandas DataFrame.
def storage2pandas(storage_file, header_shift=0):
    f = open(storage_file, 'r')
    header = 0
    for i, line in enumerate(f):
        if line.count('endheader') != 0:
            header = i
    f.close()

    data = pd.read_csv(storage_file, delimiter="\t", header=header+header_shift, low_memory=False)
    return data

# Create y-label plot labels based on the type of data (joint angles, joint
# forces and torques, or marker trajectories) and the type of motion
# (translational or rotational).
def getLabelFromMotionAndDataType(motion_type, data_type):
    label = ''
    if motion_type == 'rotational':
        if data_type == 'kinematic': label = 'angle (rad)'
        elif data_type == 'kinetic': label = 'torque (N-m)'
        elif data_type == 'marker': raise Exception('Marker data cannot be of motion type "rotational".')
        return label
    elif motion_type == 'translational':
        if data_type == 'kinematic': label = 'position (m)'
        elif data_type == 'kinetic': label = 'force (N)'
        elif data_type == 'marker': label = 'error (cm)'
        return label
    else:
        return label

# Truncate plot titles if the get too long.
def truncate(string, max_length):
    """https://www.xormedia.com/string-truncate-middle-with-ellipsis/"""
    if len(string) <= max_length:
        # string is already short-enough
        return string
    # half of the size, minus the 3 .'s
    n_2 = int(max_length / 2 - 3)
    # whatever's left
    n_1 = max_length - n_2 - 3
    return '{0}...{1}'.format(string[:n_1], string[-n_2:])


# Given a state or control name with substring identifying either the left or
# right limb, remove the substring and return the updated name. This function
# also takes the argument 'ls_dict', which is a dictionary of plot linestyles
# corresponding to the right leg (solid line) or left leg (dashed line); it is
# updated here for convenience.
def bilateralize(name, ls_dict, data_type):
    # Keep modifying the name until no side tags remain.
    isRightLeg = True
    isMarker = data_type == 'marker'
    while True:
        if '_r/' in name:
            name = name.replace('_r/', '/')
        elif '_l/' in name:
            name = name.replace('_l/', '/')
            isRightLeg = False
        elif '_r_' in name:
            name = name.replace('_r_', '_')
        elif '_l_' in name:
            name = name.replace('_l_', '_')
            isRightLeg = False
        elif name[-2:] == '_r':
            name = name[:-2]
        elif name[-2:] == '_l':
            name = name[:-2]
            isRightLeg = False
        elif name[0] == 'R' and isMarker:
            name = name[1:]
            ls_dict[name].append('-')
            break
        elif name[0] == 'L' and isMarker:
            name = name[1:]
            ls_dict[name].append('--')
            break
        else:
            if isRightLeg:
                ls_dict[name].append('-')
            else:
                ls_dict[name].append('--')

            break

    return name, ls_dict


def getIndexForNearestValue(vec, val):
    return min(range(len(vec)), key=lambda i: abs(vec[i]-val))


# Plot the DataFrame 'table' results into a PDF of figures at handle 'pdf'.
def plotTable(pdf, table, refs, colors, title_dict, ls_dict, label_dict,
              legend_handles, legend_labels, motion_type, data_type):

    # Set plot parameters.
    plots_per_page = 15.0
    num_cols = 3
    num_rows = (plots_per_page / num_cols) + 1

    # Get time column.
    time = table['time']

    # Loop through all keys in the dictionary and plot all variables.
    p = 1  # Counter to keep track of number of plots per page.
    for i, key in enumerate(title_dict.keys()):
        # If this is first key or if we filled up the previous page with
        # plots, create a new figure that will become the next page.
        if p % plots_per_page == 1:
            fig = plt.figure(figsize=(8.5, 11))

        plt.subplot(int(num_rows), int(num_cols),
                    int(p + num_cols))
        # Loop through all the state variable paths for this key.
        ymin = np.inf
        ymax = -np.inf
        handles = list()
        labels = list()
        # Is this a residual force?
        is_force = '_force' in key
        is_moment = '_moment' in key
        is_residual = ('pelvis' in key) and (is_force or is_moment)
        for path, ls in zip(title_dict[key], ls_dict[key]):
            var = table[path]
            ymin = np.minimum(ymin, np.min(var))
            ymax = np.maximum(ymax, np.max(var))

            # If any reference data was provided, that has columns matching
            # the current variable path, then plot them first.
            for r, ref in enumerate(refs):
                init = getIndexForNearestValue(ref['time'], time[0])
                final = getIndexForNearestValue(ref['time'], time[len(time)-1])
                y = ref[path][init:final]
                plt.plot(ref['time'][init:final],
                         y, ls=ls,
                         color=colors[r],
                         linewidth=2.5)
                ymin = np.minimum(ymin, np.min(y))
                ymax = np.maximum(ymax, np.max(y))

            # Plot the variable values from the MocoTrajectory.
            plt.plot(time, var, ls=ls,
                     color=colors[len(refs)],
                     linewidth=1.5,
                     zorder=4)

            # Save legend handles to report marker or residual RMSE.
            if data_type == 'marker':
                h = mlines.Line2D([], [], ls=ls,
                                  color=colors[len(refs)], linewidth=1.0)
                handles.append(h)
                rmse = np.sqrt(np.mean(var ** 2))
                labels.append(f'RMSE = {rmse:1.2f} cm')

            elif data_type == 'kinetic' and is_residual:
                h = mlines.Line2D([], [], ls=ls,
                                  color=colors[len(refs)], linewidth=1.0)
                handles.append(h)
                rmse = np.sqrt(np.mean(var ** 2))
                if is_force:
                    labels.append(f'RMSE = {rmse:1.2f} N')
                elif is_moment:
                    labels.append(f'RMSE = {rmse:1.2f} N-m')

        # Plot labels and settings.
        plt.title(truncate(key, 38), fontsize=10)
        plt.xlabel('time (s)', fontsize=8)
        plt.ylabel(label_dict[key], fontsize=8)
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        plt.xlim(time[0], time[time.size-1])
        plt.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
        ax = plt.gca()
        ax.get_yaxis().get_offset_text().set_position((-0.15, 0))
        ax.get_yaxis().get_offset_text().set_fontsize(6)
        ax.tick_params(direction='in', gridOn=True, zorder=0)
        from matplotlib.ticker import FormatStrFormatter
        ax.xaxis.set_major_formatter(
            FormatStrFormatter('%.1f'))

        # Report marker or residual RMSE in axis legend.
        if data_type == 'marker':
            if ymax > 10:
                plt.ylim(0, 2.0 * np.ceil(ymax / 2.0))
            else:
                plt.ylim(0, 10)
                plt.yticks([0, 2, 4, 6, 8, 10])

            plt.axhline(y=2, color='g', linestyle='--', zorder=3, lw=1.0)
            plt.axhline(y=4, color='r', linestyle='--', zorder=3, lw=1.0)
            plt.legend(handles, labels, fontsize=7)

        elif is_residual:
            plt.legend(handles, labels, fontsize=7)

        # If we filled up the current figure or ran out of keys, add this
        # figure as a new page to the PDF. Otherwise, increment the plot
        # counter and keep going.
        if (p % plots_per_page == 0) or (i == len(title_dict.keys()) - 1):
            legfontsize = 64 / len(legend_handles)
            if legfontsize > 10: legfontsize = 10
            fig.tight_layout()
            plt.figlegend(legend_handles, legend_labels,
                          loc='lower center',
                          bbox_to_anchor=(0.5, 0.85),
                          fancybox=True, shadow=True,
                          prop={'size': legfontsize})
            pdf.savefig(fig)
            plt.close()
            p = 1
        else:
            p += 1

# Generate a PDF report for the DataFrame 'table' at the location 'output_fpath'. Here,
# 'filename' is just used to create an appropriate legend label for the passed in table.
# The arguments 'data_type' and 'bilateral' are used to specify the appropriate axis labels
# for the plots generated by 'plotTable()' above.
def generateReportForTable(table, filename, refs, ref_files, output_fpath, data_type, bilateral=True):

    colors = list()
    import matplotlib.cm as cm
    cmap_samples = np.linspace(0.1, 0.9, len(refs))
    cmap = cm.get_cmap('viridis')
    for sample in cmap_samples:
        colors.append(cmap(sample))
    colors.append('k')

    # Suffixes to detect if a pelvis coordinate is translational or rotational.
    translate_suffixes = ['_tx', '_ty', '_tz', '_force']
    rotate_suffixes = ['_tilt', '_list', '_rotation', '_moment']

    # Create legend handles and labels that can be used to create a figure
    # legend that is applicable all figures.
    legend_handles = list()
    legend_labels = list()
    all_files = list()
    if not ref_files is None:
        all_files += ref_files
    all_files.append(filename)
    lw = 8 / len(colors)
    if lw < 0.5: lw = 0.5
    if lw > 2: lw = 2
    for color, file in zip(colors, all_files):
        if bilateral:
            r = mlines.Line2D([], [], ls='-', color=color, linewidth=lw)
            legend_handles.append(r)
            legend_labels.append(file + ' (right leg)')
            l = mlines.Line2D([], [], ls='--', color=color, linewidth=lw)
            legend_handles.append(l)
            legend_labels.append(file + ' (left leg)')
        else:
            h = mlines.Line2D([], [], ls='-', color=color, linewidth=lw)
            legend_handles.append(h)
            legend_labels.append(file)

    # Fill the dictionaries needed by plotTable().
    title_dict = OrderedDict()
    ls_dict = defaultdict(list)
    label_dict = dict()
    motion_type = 'rotational'
    for col_label in table.columns:
        if col_label == 'time': continue

        title = col_label
        if bilateral:
            title, ls_dict = bilateralize(title, ls_dict, data_type)
        else:
            ls_dict[title].append('-')
        if not title in title_dict:
            title_dict[title] = list()

        # If 'bilateral' is True, the 'title' key will
        # correspond to a list containing paths for both sides
        # of the model.
        title_dict[title].append(col_label)

        # Create the appropriate labels.
        if data_type == 'marker':
            motion_type = 'translational'
        else:
            # If we have a pelvis coordinate, detect if translational or rotational.
            if 'pelvis' in col_label:
                motion_type = ''
                for suffix in translate_suffixes:
                    if col_label.endswith(suffix):
                        motion_type = 'translational'

                for suffix in rotate_suffixes:
                    if col_label.endswith(suffix):
                        motion_type = 'rotational'

            else:
                motion_type = 'rotational'

        label_dict[title] = getLabelFromMotionAndDataType(motion_type, data_type)

    # Create a PDF instance and plot the table.
    with PdfPages(output_fpath) as pdf:
        plotTable(pdf, table, refs, colors, title_dict, ls_dict, label_dict,
                      legend_handles, legend_labels, motion_type, data_type)

# Plot joint angle results located in MOT files under results/IK.
def plotIKResults(data_fpaths, output_fpath, header_shifts):
    table = storage2pandas(data_fpaths[0], header_shift=header_shifts[0])
    refs = list()
    ref_files = list()
    for ipath, fpath in enumerate(data_fpaths):
        if ipath:
            refs.append(storage2pandas(data_fpaths[ipath], header_shift=header_shifts[ipath]))
            ref_files.append(os.path.basename(data_fpaths[ipath]))
    filename = os.path.basename(data_fpaths[0])
    data_type = 'kinematic'
    generateReportForTable(table, filename, refs, ref_files, output_fpath, data_type)

    return table, refs

# Plot joint torque results located in MOT files under results/ID.
def plotIDResults(data_fpaths, output_fpath, header_shifts):
    table = storage2pandas(data_fpaths[0], header_shift=header_shifts[0])

    temp_refs = list()
    ref_files = list()
    for ipath, fpath in enumerate(data_fpaths):
        if ipath:
            ref = storage2pandas(data_fpaths[ipath], header_shift=header_shifts[ipath])
            ref.columns = [col + '_moment' for col in ref.columns]
            ref = ref.rename(columns={'FX_moment': 'pelvis_tx_force',
                                        'FY_moment': 'pelvis_ty_force',
                                        'FZ_moment': 'pelvis_tz_force',
                                        'MX_moment': 'pelvis_list_moment',
                                        'MY_moment': 'pelvis_rotation_moment',
                                        'MZ_moment': 'pelvis_tilt_moment',
                                        'time_moment': 'time'})
            temp_refs.append(ref)
            ref_files.append(os.path.basename(data_fpaths[ipath]))

    refs = list()
    for ref in temp_refs:
        table = table[[col for col in table.columns if col in ref.columns]]
        refs.append(ref[[col for col in ref.columns if col in table.columns]])

    filename = os.path.basename(data_fpaths[0])
    data_type = 'kinetic'
    generateReportForTable(table, filename, refs, ref_files, output_fpath, data_type)

    return table, refs
#
# # Plot ground reaction force data located in MOT files under results/ID.
# def plotGRFData(data_fpath):
#     table = storage2pandas(data_fpath, header_shift=1)
#     filename = os.path.basename(data_fpath)
#     output_fpath = data_fpath.replace('.mot', '.pdf')
#     data_type = 'kinetic'
#     generateReportForTable(table, filename, output_fpath, data_type, bilateral=False)
#
# # Plot marker errors located in CSV files under results/IK.
# def plotMarkerErrors(data_fpath, ik_fpath):
#     # Load table.
#     table = pd.read_csv(data_fpath)
#
#     # Drop all timesteps RMSE row and timestep column.
#     table.drop(columns='Timestep', inplace=True)
#     table.drop(0, inplace=True)
#     table.reset_index(drop=True, inplace=True)
#
#     # Insert time column from IK results.
#     ik_table = storage2pandas(ik_fpath, header_shift=-1)
#     table.insert(0, 'time', ik_table['time'])
#
#     # Convert from m to cm.
#     table *= 100.0
#
#     # Plot marker errors.
#     filename = os.path.basename(data_fpath)
#     output_fpath = data_fpath.replace('.csv', '.pdf')
#     data_type = 'marker'
#     generateReportForTable(table, filename, output_fpath, data_type)