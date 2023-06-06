*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.82 cm
- Avg. Max Marker Error = 4.99 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 5.51 N
- Avg. Residual Torque = 35.48 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 65.34 kg (+2.09% change from original 64.0 kg)

Individual body mass changes:

  - pelvis    mass = 11.11 kg (+10.75% change from original 10.03 kg)
  - femur_r   mass = 8.11 kg (+2.42% change from original 7.92 kg)
  - tibia_r   mass = 2.49 kg (-21.12% change from original 3.16 kg)
  - talus_r   mass = 0.13 kg (+49.63% change from original 0.09 kg)
  - calcn_r   mass = 0.99 kg (-6.62% change from original 1.06 kg)
  - toes_r    mass = 0.05 kg (-74.97% change from original 0.18 kg)
  - femur_l   mass = 8.11 kg (+2.42% change from original 7.92 kg)
  - tibia_l   mass = 2.49 kg (-21.12% change from original 3.16 kg)
  - talus_l   mass = 0.13 kg (+49.63% change from original 0.09 kg)
  - calcn_l   mass = 0.99 kg (-6.62% change from original 1.06 kg)
  - toes_l    mass = 0.05 kg (-74.97% change from original 0.18 kg)
  - torso     mass = 25.38 kg (+11.10% change from original 22.84 kg)
  - humerus_r mass = 1.95 kg (+12.40% change from original 1.73 kg)
  - ulna_r    mass = 0.28 kg (-46.65% change from original 0.52 kg)
  - radius_r  mass = 0.28 kg (-46.65% change from original 0.52 kg)
  - hand_r    mass = 0.16 kg (-58.75% change from original 0.39 kg)
  - humerus_l mass = 1.95 kg (+12.40% change from original 1.73 kg)
  - ulna_l    mass = 0.28 kg (-46.65% change from original 0.52 kg)
  - radius_l  mass = 0.28 kg (-46.65% change from original 0.52 kg)
  - hand_l    mass = 0.16 kg (-58.75% change from original 0.39 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 2.04 cm
  - Avg. Marker Max Error = 5.83 cm
  - Avg. Residual Force   = 4.01 N
  - Avg. Residual Torque  = 42.78 N-m
  - WARNING: 2 marker(s) with RMSE greater than 4 cm!
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.37 cm
  - Avg. Marker Max Error = 3.02 cm
  - Avg. Residual Force   = 5.04 N
  - Avg. Residual Torque  = 20.27 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.82 cm
  - Avg. Marker Max Error = 4.98 cm
  - Avg. Residual Force   = 8.71 N
  - Avg. Residual Torque  = 29.51 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 2.11 cm
  - Avg. Marker Max Error = 6.48 cm
  - Avg. Residual Force   = 3.94 N
  - Avg. Residual Torque  = 52.84 N-m
  - WARNING: 3 marker(s) with RMSE greater than 4 cm!
  --> See IK/run500_ik_summary.txt and ID/run500_id_summary.txt for more details.


The model file containing optimal body scaling, marker offsets, and
mass parameters is:

Models/final.osim

This tool works by finding optimal scale factors and marker offsets at
the same time. If specified, it also runs a second optimization to
find mass parameters to fit the model dynamics to the ground reaction
force data.

The model containing the optimal body scaling and marker offsets found
prior to the dynamics fitting step is:

Models/optimized_scale_and_markers.osim

If you want to manually edit the marker offsets, you can modify the
<MarkerSet> in "Models/unscaled_but_with_optimized_markers.osim" (by
default this file contains the marker offsets found by the optimizer).
If you want to tweak the Scaling, you can edit
"Models/rescaling_setup.xml". If you change either of these files,
then run (FROM THE "Models" FOLDER, and not including the leading ">
"):

 > opensim-cmd run-tool rescaling_setup.xml
           # This will re-generate Models/optimized_scale_and_markers.osim


You do not need to re-run Inverse Kinematics unless you change
scaling, because the output motion files are already generated for you
as "*_ik.mot" files for each trial, but you are welcome to confirm our
results using OpenSim. To re-run Inverse Kinematics with OpenSim, to
verify the results of AddBiomechanics, you can use the automatically
generated XML configuration files. Here are the command-line commands
you can run (FROM THE "IK" FOLDER, and not including the leading "> ")
to verify IK results for each trial:

 > opensim-cmd run-tool run400_ik_setup.xml
           # This will create a results file IK/run400_ik_by_opensim.mot
 > opensim-cmd run-tool run200_ik_setup.xml
           # This will create a results file IK/run200_ik_by_opensim.mot
 > opensim-cmd run-tool run300_ik_setup.xml
           # This will create a results file IK/run300_ik_by_opensim.mot
 > opensim-cmd run-tool run500_ik_setup.xml
           # This will create a results file IK/run500_ik_by_opensim.mot


To re-run Inverse Dynamics using OpenSim, you can also use
automatically generated XML configuration files. WARNING: Inverse
Dynamics in OpenSim uses a different time-step definition to the one
used in AddBiomechanics (AddBiomechanics uses semi-implicit Euler,
OpenSim uses splines). This means that your OpenSim inverse dynamics
results WILL NOT MATCH your AddBiomechanics results, and YOU SHOULD
NOT EXPECT THEM TO. The following commands should work (FROM THE "ID"
FOLDER, and not including the leading "> "):

 > opensim-cmd run-tool run400_id_setup.xml
           # This will create results on time range (0.12s to 2.05s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.21s to 2.37s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.47s to 2.58s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.34s to 2.14s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics