*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.59 cm
- Avg. Max Marker Error = 4.40 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 6.59 N
- Avg. Residual Torque = 10.96 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 95.26 kg (+2.54% change from original 92.9 kg)

Individual body mass changes:

  - pelvis    mass = 21.21 kg (+45.75% change from original 14.56 kg)
  - femur_r   mass = 12.75 kg (+10.94% change from original 11.50 kg)
  - tibia_r   mass = 3.15 kg (-31.30% change from original 4.58 kg)
  - talus_r   mass = 0.04 kg (-65.19% change from original 0.12 kg)
  - calcn_r   mass = 1.05 kg (-32.00% change from original 1.54 kg)
  - toes_r    mass = 0.05 kg (-81.86% change from original 0.27 kg)
  - femur_l   mass = 12.75 kg (+10.94% change from original 11.50 kg)
  - tibia_l   mass = 3.15 kg (-31.30% change from original 4.58 kg)
  - talus_l   mass = 0.04 kg (-65.19% change from original 0.12 kg)
  - calcn_l   mass = 1.05 kg (-32.00% change from original 1.54 kg)
  - toes_l    mass = 0.05 kg (-81.86% change from original 0.27 kg)
  - torso     mass = 31.75 kg (-4.25% change from original 33.16 kg)
  - humerus_r mass = 1.62 kg (-35.71% change from original 2.51 kg)
  - ulna_r    mass = 0.64 kg (-14.21% change from original 0.75 kg)
  - radius_r  mass = 0.64 kg (-14.21% change from original 0.75 kg)
  - hand_r    mass = 1.20 kg (+112.20% change from original 0.57 kg)
  - humerus_l mass = 1.62 kg (-35.71% change from original 2.51 kg)
  - ulna_l    mass = 0.64 kg (-14.21% change from original 0.75 kg)
  - radius_l  mass = 0.64 kg (-14.21% change from original 0.75 kg)
  - hand_l    mass = 1.20 kg (+112.20% change from original 0.57 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: walking2
  - Avg. Marker RMSE      = 1.73 cm
  - Avg. Marker Max Error = 3.96 cm
  - Avg. Residual Force   = 2.69 N
  - Avg. Residual Torque  = 9.90 N-m
  --> See IK/walking2_ik_summary.txt and ID/walking2_id_summary.txt for more details.

trial: walkingTS3
  - Avg. Marker RMSE      = 1.70 cm
  - Avg. Marker Max Error = 4.30 cm
  - Avg. Residual Force   = 2.60 N
  - Avg. Residual Torque  = 8.75 N-m
  --> See IK/walkingTS3_ik_summary.txt and ID/walkingTS3_id_summary.txt for more details.

trial: squats1
  - Avg. Marker RMSE      = 1.45 cm
  - Avg. Marker Max Error = 4.28 cm
  - Avg. Residual Force   = 2.47 N
  - Avg. Residual Torque  = 7.10 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/squats1_ik_summary.txt and ID/squats1_id_summary.txt for more details.

trial: walkingTS1
  - Avg. Marker RMSE      = 1.78 cm
  - Avg. Marker Max Error = 4.36 cm
  - Avg. Residual Force   = 1.32 N
  - Avg. Residual Torque  = 9.17 N-m
  --> See IK/walkingTS1_ik_summary.txt and ID/walkingTS1_id_summary.txt for more details.

trial: walking3
  - Avg. Marker RMSE      = 1.67 cm
  - Avg. Marker Max Error = 3.99 cm
  - Avg. Residual Force   = 2.51 N
  - Avg. Residual Torque  = 7.74 N-m
  --> See IK/walking3_ik_summary.txt and ID/walking3_id_summary.txt for more details.

trial: walkingTS2
  - Avg. Marker RMSE      = 1.71 cm
  - Avg. Marker Max Error = 4.24 cm
  - Avg. Residual Force   = 0.97 N
  - Avg. Residual Torque  = 8.52 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/walkingTS2_ik_summary.txt and ID/walkingTS2_id_summary.txt for more details.

trial: DJ5
  - Avg. Marker RMSE      = 2.35 cm
  - Avg. Marker Max Error = 7.30 cm
  - Avg. Residual Force   = 80.28 N
  - Avg. Residual Torque  = 65.90 N-m
  - WARNING: 3 marker(s) with RMSE greater than 4 cm!
  - WARNING: Automatic data processing required modifying TRC data from 2 marker(s)!
  --> See IK/DJ5_ik_summary.txt and ID/DJ5_id_summary.txt for more details.

trial: walking4
  - Avg. Marker RMSE      = 1.67 cm
  - Avg. Marker Max Error = 3.99 cm
  - Avg. Residual Force   = 2.69 N
  - Avg. Residual Torque  = 8.58 N-m
  --> See IK/walking4_ik_summary.txt and ID/walking4_id_summary.txt for more details.


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

 > opensim-cmd run-tool walking2_ik_setup.xml
           # This will create a results file IK/walking2_ik_by_opensim.mot
 > opensim-cmd run-tool walkingTS3_ik_setup.xml
           # This will create a results file IK/walkingTS3_ik_by_opensim.mot
 > opensim-cmd run-tool squats1_ik_setup.xml
           # This will create a results file IK/squats1_ik_by_opensim.mot
 > opensim-cmd run-tool walkingTS1_ik_setup.xml
           # This will create a results file IK/walkingTS1_ik_by_opensim.mot
 > opensim-cmd run-tool walking3_ik_setup.xml
           # This will create a results file IK/walking3_ik_by_opensim.mot
 > opensim-cmd run-tool walkingTS2_ik_setup.xml
           # This will create a results file IK/walkingTS2_ik_by_opensim.mot
 > opensim-cmd run-tool DJ5_ik_setup.xml
           # This will create a results file IK/DJ5_ik_by_opensim.mot
 > opensim-cmd run-tool walking4_ik_setup.xml
           # This will create a results file IK/walking4_ik_by_opensim.mot


To re-run Inverse Dynamics using OpenSim, you can also use
automatically generated XML configuration files. WARNING: Inverse
Dynamics in OpenSim uses a different time-step definition to the one
used in AddBiomechanics (AddBiomechanics uses semi-implicit Euler,
OpenSim uses splines). This means that your OpenSim inverse dynamics
results WILL NOT MATCH your AddBiomechanics results, and YOU SHOULD
NOT EXPECT THEM TO. The following commands should work (FROM THE "ID"
FOLDER, and not including the leading "> "):

 > opensim-cmd run-tool walking2_id_setup.xml
           # This will create results on time range (0.01s to 1.34s) in file ID/walking2_osim_id.sto
 > opensim-cmd run-tool walkingTS3_id_setup.xml
           # This will create results on time range (0.01s to 1.58s) in file ID/walkingTS3_osim_id.sto
 > opensim-cmd run-tool squats1_id_setup.xml
           # This will create results on time range (0.01s to 13.47s) in file ID/squats1_osim_id.sto
 > opensim-cmd run-tool walkingTS1_id_setup.xml
           # This will create results on time range (0.01s to 1.61s) in file ID/walkingTS1_osim_id.sto
 > opensim-cmd run-tool walking3_id_setup.xml
           # This will create results on time range (0.01s to 1.34s) in file ID/walking3_osim_id.sto
 > opensim-cmd run-tool walkingTS2_id_setup.xml
           # This will create results on time range (0.01s to 1.56s) in file ID/walkingTS2_osim_id.sto
 > opensim-cmd run-tool DJ5_id_setup.xml
           # This will create results on time range (1.19s to 2.46s) in file ID/DJ5_osim_id.sto
 > opensim-cmd run-tool walking4_id_setup.xml
           # This will create results on time range (0.01s to 1.36s) in file ID/walking4_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics