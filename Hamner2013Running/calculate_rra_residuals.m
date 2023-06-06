%% calculate_rra_residuals.m
% calculate residuals relative to external force and external force * 
% center of mass height magnitudes across all trials.
warning('off','MATLAB:table:ModifiedAndSavedVarnames');
clear all;

%% user inputs
demographics_filepath = 'demographics.csv';
source = 'hamner';
waveforms_filepath = ['residuals/' source '/'];

if strcmp(source, 'addbio')
    residual_force_names = {'pelvis_tx_force','pelvis_ty_force','pelvis_tz_force'};
    residual_moment_names = {'pelvis_list_moment','pelvis_rotation_moment','pelvis_tilt_moment'};
elseif strcmp(source, 'hamner')
    residual_force_names = {'FX','FY','FZ'};
    residual_moment_names = {'MX','MY','MZ'};

end

% read subject list
demographics = readtable(demographics_filepath);
subjectIDs = demographics.subject;
subject_masses = demographics.weight_kg_;

n_subjects = length(subjectIDs);
raw_peak_forces = zeros(n_subjects,1);
raw_rms_forces = zeros(n_subjects,1);
raw_peak_moments = zeros(n_subjects,1);
raw_rms_moments = zeros(n_subjects,1);
mass_normalized_peak_forces = zeros(n_subjects,1);
mass_normalized_rms_forces = zeros(n_subjects,1);
mass_normalized_peak_moments = zeros(n_subjects,1);
mass_normalized_rms_moments = zeros(n_subjects,1);
kinetic_normalized_peak_forces = zeros(n_subjects,1);
kinetic_normalized_rms_forces = zeros(n_subjects,1);
kinetic_normalized_peak_moments = zeros(n_subjects,1);
kinetic_normalized_rms_moments = zeros(n_subjects,1);
for i = 1:n_subjects
    subjectID = char(subjectIDs{i});
    subject_mass = subject_masses(i); % kg
    
    % trial filenames associated with this subjectID
    residuals_by_trial = dir([waveforms_filepath subjectID '_run*_residuals.sto']);
    
    n_trials = length(residuals_by_trial);

    subject_raw_peak_forces = zeros(n_trials,1);
    subject_raw_rms_forces = zeros(n_trials,1);
    subject_raw_peak_moments = zeros(n_trials,1);
    subject_raw_rms_moments = zeros(n_trials,1);
    
    subject_mass_normalized_peak_forces = zeros(n_trials,1);
    subject_mass_normalized_rms_forces = zeros(n_trials,1);
    subject_mass_normalized_peak_moments = zeros(n_trials,1);
    subject_mass_normalized_rms_moments = zeros(n_trials,1);
    
    subject_kinetic_normalized_peak_forces = zeros(n_trials,1);
    subject_kinetic_normalized_rms_forces = zeros(n_trials,1);
    subject_kinetic_normalized_peak_moments = zeros(n_trials,1);
    subject_kinetic_normalized_rms_moments = zeros(n_trials,1);
    
    % loop over trials for subject
    for j = 1:n_trials
        % read waveform data
        filename = residuals_by_trial(j).name;
        [res_forces, res_moments] = get_residuals([waveforms_filepath filename], ...
            residual_force_names, residual_moment_names);

        subject_raw_peak_forces(j) = max(res_forces);
        subject_raw_rms_forces(j) = compute_rmse(res_forces, 0);
        subject_raw_peak_moments(j) = max(res_moments);
        subject_raw_rms_moments(j) = compute_rmse(res_moments, 0);
            
        % get normalized peak and rms residuals and append to subject data        
        mass_normalized_res_forces = res_forces / subject_mass;
        mass_normalized_res_moments = res_moments / subject_mass;
        
        subject_mass_normalized_peak_forces(j) = max(mass_normalized_res_forces);
        subject_mass_normalized_rms_forces(j) = compute_rmse(mass_normalized_res_forces, 0);
        subject_mass_normalized_peak_moments(j) = max(mass_normalized_res_moments);
        subject_mass_normalized_rms_moments(j) = compute_rmse(mass_normalized_res_moments, 0);
        
        % get peak and rms residuals as percentages of net external force
        % and COM height. Note: 'max_ext_mom' = mean COM height * max
        % external force magnitude
        com_filename = [waveforms_filepath filename(1:end-13) 'com.sto'];
        grf_filename = [waveforms_filepath filename(1:end-13) 'grf.mot'];
        [max_ext_force, max_ext_moment] = get_external_kinetics(com_filename, grf_filename, source);
        
        kinetic_normalized_res_forces = reshape(res_forces, 1, 101) / max_ext_force;        
        kinetic_normalized_res_moments = reshape(res_moments, 1, 101) / max_ext_moment;
        
        subject_kinetic_normalized_peak_forces(j) = max(kinetic_normalized_res_forces);
        subject_kinetic_normalized_rms_forces(j) = compute_rmse(kinetic_normalized_res_forces, 0);
        subject_kinetic_normalized_peak_moments(j) = max(kinetic_normalized_res_moments);
        subject_kinetic_normalized_rms_moments(j) = compute_rmse(kinetic_normalized_res_moments, 0);
    end
    
    % append trial averages
    raw_peak_forces(i) = mean(subject_raw_peak_forces);
    raw_rms_forces(i) = mean(subject_raw_rms_forces);
    raw_peak_moments(i) = mean(subject_raw_peak_moments);
    raw_rms_moments(i) = mean(subject_raw_rms_moments);

    mass_normalized_peak_forces(i) = mean(subject_mass_normalized_peak_forces);
    mass_normalized_rms_forces(i) = mean(subject_mass_normalized_rms_forces);
    mass_normalized_peak_moments(i) = mean(subject_mass_normalized_peak_moments);
    mass_normalized_rms_moments(i) = mean(subject_mass_normalized_rms_moments);
    
    kinetic_normalized_peak_forces(i) = mean(subject_kinetic_normalized_peak_forces);
    kinetic_normalized_rms_forces(i) = mean(subject_kinetic_normalized_rms_forces);
    kinetic_normalized_peak_moments(i) = mean(subject_kinetic_normalized_peak_moments);
    kinetic_normalized_rms_moments(i) = mean(subject_kinetic_normalized_rms_moments);
end

demographics.raw_peak_forces = raw_peak_forces;
demographics.raw_rms_forces = raw_rms_forces;
demographics.raw_peak_moments = raw_peak_moments;
demographics.raw_rms_moments = raw_rms_moments;

demographics.mass_normalized_peak_forces = mass_normalized_peak_forces;
demographics.mass_normalized_rms_forces = mass_normalized_rms_forces;
demographics.mass_normalized_peak_moments = mass_normalized_peak_moments;
demographics.mass_normalized_rms_moments = mass_normalized_rms_moments;

demographics.kinetic_normalized_peak_forces = kinetic_normalized_peak_forces;
demographics.kinetic_normalized_rms_forces = kinetic_normalized_rms_forces;
demographics.kinetic_normalized_peak_moments = kinetic_normalized_peak_moments;
demographics.kinetic_normalized_rms_moments = kinetic_normalized_rms_moments;

fprintf('\n')
fprintf(['Normalized residuals summary for source "' source '"\n'])
fprintf('-------------------------------------------\n')
fprintf('Max Force Res: %.1f%% \x00B1 %.1f%% External Force\n', ...
    100*mean(kinetic_normalized_peak_forces), 100*std(kinetic_normalized_peak_forces));
fprintf('Res Force RMSE: %.1f%% \x00B1 %.1f%% External Force\n', ...
    100*mean(kinetic_normalized_rms_forces), 100*std(kinetic_normalized_rms_forces));
fprintf('Max Moment Res: %.1f%% \x00B1 %.1f%% COM Height * External Force\n', ...
    100*mean(kinetic_normalized_peak_moments), 100*std(kinetic_normalized_peak_moments));
fprintf('Res Moment RMSE: %.1f%% \x00B1 %.1f%% COM Height * External Force\n', ...
    100*mean(kinetic_normalized_rms_moments), 100*std(kinetic_normalized_rms_moments));

fprintf('\n')
fprintf(['Raw residuals summary for source "' source '"\n'])
fprintf('-------------------------------------------\n')
fprintf('Max Force Res: %.1f \x00B1 %.1f N\n', ...
    mean(raw_peak_forces), std(raw_peak_forces));
fprintf('Res Force RMSE: %.1f \x00B1 %.1f N\n', ...
    mean(raw_rms_forces), std(raw_rms_forces));
fprintf('Max Moment Res: %.1f \x00B1 %.1f N-m\n', ...
    mean(raw_peak_moments), std(raw_peak_moments));
fprintf('Res Moment RMSE: %.1f \x00B1 %.1f N-m\n', ...
    mean(raw_rms_moments), std(raw_rms_moments));

%% Write results
writetable(demographics, ['residuals_summary_' source '.csv']);

%% Helpers

function [res_forces, res_moms] = get_residuals(filename, ...
        residual_force_names, residual_moment_names)
    % extract residuals for the given trial.
    %
    % Args:
    %   filename (str): .sto file containing residual waveforms.
    %
    % Returns:
    %   res_forces (array): vector of residual force magnitude over the
    %                       trial.
    %   res_moms (array): vector of residual moment magnitude over the
    %                     trial.
    
    residuals = readtable(filename, 'filetype', 'text');
    residuals_forces = table2array(residuals(:, residual_force_names));
    residuals_moments = table2array(residuals(:, residual_moment_names));
    
    res_forces = vecnorm(residuals_forces, 2, 2);
    res_moms = vecnorm(residuals_moments, 2, 2);
    
    % resample to 101 points
    res_forces = interp1(1:length(res_forces), res_forces, ...
        linspace(1, length(res_forces), 101));
    res_moms = interp1(1:length(res_moms), res_moms, ...
        linspace(1, length(res_moms), 101));
end

function [max_ext_force, max_ext_mom] = get_external_kinetics(com_filename, grf_filename, source)
    % get maximum external force and maximum external force * center of
    % mass height values across the trial.
    %
    % Args:
    %   com_filename (str): .sto file containing COM waveforms.
    %   grf_filename (str): .mot file containing filtered GRF waveforms.
    %
    % Returns:
    %   max_ext_force (float): maximum external force magnitude.
    %   max_ext_mom (float): maximum value of external force magnitude *
    %                        mean center of mass height.
    %
    % Notes:
    %   ext_moms aren't exactly external moments. They are COM height *
    %   external force magnitude.
    
    positions = readtable(com_filename, 'filetype', 'text');
    times = table2array(positions(:, {'time'}));
    start = times(1);
    stop = times(end);
    com_heights = table2array(positions(:, {'center_of_mass_Y'}));
    % resample to 101 points
    mean_com_height = mean(com_heights);
    
    % external forces
    forces = readtable(grf_filename, 'filetype', 'text');
    times = table2array(forces(:, {'time'}));
    if strcmp(source, 'addbio')
        forces_1 = table2array(forces(:, {'ground_force_calcn_r_vx', ...
            'ground_force_calcn_r_vy', 'ground_force_calcn_r_vz'}));
        forces_2 = table2array(forces(:, {'ground_force_calcn_l_vx', ...
            'ground_force_calcn_l_vy','ground_force_calcn_l_vz'}));
        
        forces = forces_1 + forces_2;
    else
        forces_1 = table2array(forces(:, {'R_ground_force_vx', ...
            'R_ground_force_vy', 'R_ground_force_vz'}));
        forces_2 = table2array(forces(:, {'L_ground_force_vx', ...
            'L_ground_force_vy', 'L_ground_force_vz'}));
        
        forces = forces_1 + forces_2;
    end

        
    % keep only relevant times and resample to 101 points
    forces = interp1(times, forces, linspace(start, stop, 101));
    
    ext_forces = vecnorm(forces, 2, 2);
    
    max_ext_force = max(ext_forces);
    max_ext_mom = mean_com_height * max_ext_force;
    % note not exactly external moment; magnitude of force * COM height
end

function rmse = compute_rmse(yhat, y)
    % compute the root-mean-square error.
    %
    % Args:
    %   yhat (array): estimates.
    %   y (array): observations.
    %
    % Returns:
    %   rmse (float): root-mean-square error.
    
    rmse = sqrt(mean((y - yhat).^2));
end
