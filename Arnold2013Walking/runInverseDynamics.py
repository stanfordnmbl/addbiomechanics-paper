import os
import opensim as osim
import numpy as np
import subprocess
import shutil
import pandas as pd
from helpers import create_markers_table, create_external_loads_table_for_gait, \
                    create_coordinates_from_solution, create_model_processor, \
                    fill_analysis_template, fill_extloads_template, fill_id_template, \
                    create_static_trial_markers, create_contact_sphere_force_table

demographics_df = pd.read_csv('demographics.csv')
subjects = demographics_df['subject']
masses = demographics_df['weight (kg)']
heights = demographics_df['height (m)']

lockFeet = True
for subject in subjects:

    # Create subject folders.
    if not os.path.isdir(os.path.join('ID', subject)):
        os.mkdir(os.path.join('ID', subject))

    # Modified model file.
    model_fpath = os.path.join('Raw', subject, f'{subject}_final.osim')
    modelProcessor = create_model_processor(model_fpath, external_loads_fpath=None, remove_forces=True,
                                            lock_feet=lockFeet)
    model = modelProcessor.process()
    model.printToXML(os.path.join('ID', subject, f'{subject}.osim'))

    # Create synthetic ground reaction forces file.
    unperturbed_fpath = os.path.join('Raw', subject, 'unperturbed.sto')
    model_fpath = os.path.join('Raw', subject, f'{subject}_final.osim')
    modelProcessor = create_model_processor(model_fpath)
    model = modelProcessor.process()
    table = create_external_loads_table_for_gait(model, unperturbed_fpath)
    sto = osim.STOFileAdapter()
    grf_id_fpath = os.path.join('ID', subject, 'grf.mot')
    sto.write(table, grf_id_fpath)

    # Create coordinates file.
    coordinates = create_coordinates_from_solution(unperturbed_fpath)
    sto.write(coordinates, os.path.join('ID', subject, 'coordinates.sto'))

    # Start and end time.
    time = np.array(coordinates.getIndependentColumn())
    start_time = time[0]
    end_time = time[-1]

    # Fill the external loads template.
    template_fpath = os.path.join('templates/external_loads.xml')
    extloads_fpath = os.path.join('ID', subject, 'external_loads.xml')
    fill_extloads_template(template_fpath, extloads_fpath, subject)

    # Fill the inverse dynamics template.
    template_fpath = os.path.join('templates/setup_id.xml')
    setup_fpath = os.path.join('ID', subject, 'setup_id.xml')
    fill_id_template(template_fpath, setup_fpath, subject, start_time, end_time)

    # Fill the analysis template.
    template_fpath = os.path.join('templates/setup_analysis.xml')
    setup_fpath = os.path.join('ID', subject, 'setup_analysis.xml')
    fill_analysis_template(template_fpath, setup_fpath, subject, 'Analysis',
                           start_time, end_time, 'external_loads.xml', 'coordinates.sto')

# Run the OpenSim analyses.
for subject in subjects:
    # Run the Analysis tool.
    p = subprocess.Popen(['opensim-cmd', 'run-tool', 'setup_analysis.xml'], cwd=os.path.join('ID', subject))
    p.wait()

    # Run the InverseDynamics tool.
    id_setup_fpath = os.path.join('setup_id.xml')
    p = subprocess.Popen(['opensim-cmd', 'run-tool', id_setup_fpath], cwd=os.path.join('ID', subject))
    p.wait()

# Copy the results to the residuals folder.
for subject in subjects:
    grf_src = os.path.join('ID', subject, 'grf.mot')
    grf_dst = os.path.join('residuals', 'id', f'{subject}_walk2_grf.mot')
    shutil.copyfile(grf_src, grf_dst)

    id_src = os.path.join('ID', subject, 'inverse_dynamics.sto')
    id_dst = os.path.join('residuals', 'id', f'{subject}_walk2_residuals.sto')
    shutil.copyfile(id_src, id_dst)

    com_src = os.path.join('ID', subject, 'Analysis', f'analysis_{subject}_walk2_BodyKinematics_pos_global.sto')
    com_dst = os.path.join('residuals', 'id', f'{subject}_walk2_com.sto')
    shutil.copyfile(com_src, com_dst)