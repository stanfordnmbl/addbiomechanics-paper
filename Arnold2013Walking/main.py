import os
import opensim as osim
import numpy as np
import subprocess
import shutil
from helpers import create_markers_table, create_external_loads_table_for_gait, \
                    create_coordinates_from_solution, create_model_processor, \
                    fill_analysis_template, fill_extloads_template, fill_id_template, \
                    create_static_trial_markers


includeStatic = False
subjects = ['subject01', 'subject02', 'subject04', 'subject18', 'subject19']
for subject in subjects:

    # Create subject folders.
    if not os.path.isdir(os.path.join('ID', subject)):
        os.mkdir(os.path.join('ID', subject))
    if not os.path.isdir(os.path.join('Formatted', subject)):
        os.mkdir(os.path.join('Formatted', subject))
    if not os.path.isdir(os.path.join('Formatted', subject, 'trials')):
        os.mkdir(os.path.join('Formatted', subject, 'trials'))
    if not os.path.isdir(os.path.join('Formatted', subject, 'trials', 'walk2')):
        os.mkdir(os.path.join('Formatted', subject, 'trials', 'walk2'))
    if includeStatic:
        if not os.path.isdir(os.path.join('Formatted', subject, 'trials', 'static')):
            os.mkdir(os.path.join('Formatted', subject, 'trials', 'static'))

    # Modified model file.
    model_fpath = os.path.join('Raw', subject, f'{subject}_final.osim')
    modelProcessor = create_model_processor(model_fpath, external_loads_fpath=None, remove_forces=True)
    model = modelProcessor.process()
    model.printToXML(os.path.join('ID', subject, f'{subject}.osim'))

    # Generic file for AddBiomechanics.
    model_src = os.path.join('Raw', 'generic_model_prescale_markers.osim')
    model_dst = os.path.join('Formatted', subject, 'unscaled_generic.osim')
    shutil.copyfile(model_src, model_dst)

    # Create synthetic ground reaction forces file.
    unperturbed_fpath = os.path.join('Raw', subject, 'unperturbed.sto')
    table = create_external_loads_table_for_gait(model_fpath, unperturbed_fpath)
    sto = osim.STOFileAdapter()
    grf_id_fpath = os.path.join('ID', subject, 'grf.mot')
    sto.write(table, grf_id_fpath)
    grf_fpath = os.path.join('Formatted', subject, 'trials', 'walk2', 'grf.mot')
    sto.write(table, grf_fpath)

    # Create synthetic markers file.
    markers = create_markers_table(model_fpath, unperturbed_fpath)
    trc_fpath = os.path.join('Formatted', subject, 'trials', 'walk2', 'markers.trc')
    trc = osim.TRCFileAdapter()
    trc.write(markers, trc_fpath)

    if includeStatic:
        # Create static trial markers file.
        static_markers = create_static_trial_markers(model_fpath)
        static_trc_fpath = os.path.join('Formatted', subject, 'trials', 'static', 'markers.trc')
        trc.write(static_markers, static_trc_fpath)

    # Create coordinates file.
    coordinates = create_coordinates_from_solution(unperturbed_fpath)
    sto.write(coordinates, os.path.join('ID', subject, 'coordinates.sto'))

    # Start and end time.
    time = np.array(coordinates.getIndependentColumn())
    start_time = time[0]
    end_time = time[-1]

    # Fill the external loads template.
    template_fpath = os.path.join('templates/external_loads.xml')
    extloads_fpath = os.path.join('ID', subject, 'templates/external_loads.xml')
    fill_extloads_template(template_fpath, extloads_fpath, subject)

    # Fill the inverse dynamics template.
    template_fpath = os.path.join('templates/setup_id.xml')
    setup_fpath = os.path.join('ID', subject, 'templates/setup_id.xml')
    fill_id_template(template_fpath, setup_fpath, subject, start_time, end_time)

    # Fill the analysis template.
    template_fpath = os.path.join('templates/setup_analysis.xml')
    setup_fpath = os.path.join('ID', subject, 'templates/setup_analysis.xml')
    fill_analysis_template(template_fpath, setup_fpath, subject, 'Analysis',
                           start_time, end_time, 'external_loads.xml', 'coordinates.sto')

    # Create directories under Processed.
    if not os.path.isdir(os.path.join('Processed', 'marker_fitting_only')):
        os.mkdir(os.path.join('Processed', 'marker_fitting_only'))
    if not os.path.isdir(os.path.join('Processed', 'marker_fitting_only', subject)):
        os.mkdir(os.path.join('Processed', 'marker_fitting_only', subject))
    if not os.path.isdir(os.path.join('Processed', 'dynamics_fitting')):
        os.mkdir(os.path.join('Processed', 'dynamics_fitting'))
    if not os.path.isdir(os.path.join('Processed', 'dynamics_fitting', subject)):
        os.mkdir(os.path.join('Processed', 'dynamics_fitting', subject))


# # Run the OpenSim analyses.
# for subject in subjects:
#     # Run the Analysis tool.
#     p = subprocess.Popen(['opensim-cmd', 'run-tool', 'setup_analysis.xml'], cwd=os.path.join('ID', subject))
#     p.wait()
#
#     # Run the InverseDynamics tool.
#     id_setup_fpath = os.path.join('setup_id.xml')
#     p = subprocess.Popen(['opensim-cmd', 'run-tool', id_setup_fpath], cwd=os.path.join('ID', subject))
#     p.wait()
#
# # Copy the results to the residuals folder.
# for subject in subjects:
#     grf_src = os.path.join('ID', subject, 'grf.mot')
#     grf_dst = os.path.join('residuals', 'id', f'{subject}_walk2_grf.mot')
#     shutil.copyfile(grf_src, grf_dst)
#
#     id_src = os.path.join('ID', subject, 'inverse_dynamics.sto')
#     id_dst = os.path.join('residuals', 'id', f'{subject}_walk2_residuals.sto')
#     shutil.copyfile(id_src, id_dst)
#
#     com_src = os.path.join('ID', subject, 'Analysis', f'analysis_{subject}_walk2_BodyKinematics_pos_global.sto')
#     com_dst = os.path.join('residuals', 'id', f'{subject}_walk2_com.sto')
#     shutil.copyfile(com_src, com_dst)


# states = run_timestepping_problem(subject, model_fpath, external_loads_fpath, unperturbed_fpath)
# sto.write(states, 'states.sto')

