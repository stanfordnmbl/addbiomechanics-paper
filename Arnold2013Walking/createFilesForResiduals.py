import pandas as pd
import os
import opensim as osim
import sys


def fill_analysis_template(template, setup, trial, model, results,
                           startTime, endTime, extLoads, coordinates):
    ft = open(template)
    content = ft.read()
    content = content.replace('@TRIAL@', trial)
    content = content.replace('@MODEL@', model)
    content = content.replace('@RESULTS_DIR@', results)
    content = content.replace('@START_TIME@', f'{startTime:.4f}')
    content = content.replace('@END_TIME@', f'{endTime:.4f}')
    content = content.replace('@EXT_LOADS@', extLoads)
    content = content.replace('@COORDINATES@', coordinates)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


def createFilesForResiduals():

    if not os.path.isdir(os.path.join('residuals')):
        os.mkdir(os.path.join('residuals'))
    if not os.path.isdir(os.path.join('residuals', 'addbio')):
        os.mkdir(os.path.join('residuals', 'addbio'))

    demographics_df = pd.read_csv('demographics.csv')

    subjects = demographics_df['subject']
    masses = demographics_df['weight (kg)']
    heights = demographics_df['height (m)']
    trials = ['walk2']
    for subject, mass, height in zip(subjects, masses, heights):

        # Create Analysis folder
        analysis_fpath = os.path.join('Processed', subject, 'osim_results', 'Analysis')
        if not os.path.isdir(analysis_fpath):
            os.mkdir(analysis_fpath)

        # Loop over all trials for this subject
        for trial in trials:

            # File paths
            grf_fpath = os.path.join('Processed', subject, 'osim_results', 'ID', f'{trial}_grf.mot')
            id_fpath = os.path.join('Processed', subject, 'osim_results', 'ID', f'{trial}_id.sto')

            # Get start and end times for AnalyzeTool
            table = osim.TimeSeriesTable(id_fpath)
            time = table.getIndependentColumn()
            startTime = time[0]
            endTime = time[table.getNumRows()-1]

            # Fill and write Analysis setup file template
            template_fpath = os.path.join('templates/setup_analysis.xml')
            setup_fpath = os.path.join('Processed', subject, 'osim_results', 'Analysis',
                                       f'{subject}_{trial}_setupAnalysis.xml')

            model_fpath = os.path.join('Processed', subject, 'osim_results', 'Models', 'final.osim')
            results_fpath = os.path.join('Processed', subject, 'osim_results', 'Analysis', f'results_{trial}')
            coordinates_fpath = os.path.join('Processed', subject, 'osim_results', 'IK', f'{trial}_ik.mot')
            extloads_fpath = os.path.join('Processed', subject, 'osim_results', 'ID', f'{trial}_external_forces.xml')
            fill_analysis_template(
                template_fpath, setup_fpath, trial,
                os.path.relpath(model_fpath, analysis_fpath),
                os.path.relpath(results_fpath, analysis_fpath),
                startTime, endTime,
                os.path.relpath(extloads_fpath, analysis_fpath),
                os.path.relpath(coordinates_fpath, analysis_fpath))

            # Run Analysis to compute center of mass trajectories
            analyze = osim.AnalyzeTool(setup_fpath)
            analyze.run()

            # Load files
            grf = osim.TimeSeriesTable(grf_fpath)
            id = osim.TimeSeriesTable(id_fpath)
            com = osim.TimeSeriesTable(os.path.join(results_fpath, f'analysis_{trial}_BodyKinematics_pos_global.sto'))

            # Write all files
            sto = osim.STOFileAdapter()
            sto.write(grf, os.path.join('residuals', 'addbio', f'{subject}_{trial}_grf.mot'))
            sto.write(id, os.path.join('residuals', 'addbio', f'{subject}_{trial}_residuals.sto'))
            sto.write(com, os.path.join('residuals', 'addbio', f'{subject}_{trial}_com.sto'))


if __name__ == '__main__':
    createFilesForResiduals()