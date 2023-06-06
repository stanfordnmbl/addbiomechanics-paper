*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.50 cm
- Avg. Max Marker Error = 3.53 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 10.90 N
- Avg. Residual Torque = 8.14 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 66.82 kg (+5.23% change from original 63.5 kg)

Individual body mass changes:

  - pelvis    mass = 17.07 kg (+71.58% change from original 9.95 kg)
  - femur_r   mass = 9.07 kg (+15.46% change from original 7.86 kg)
  - tibia_r   mass = 2.09 kg (-33.14% change from original 3.13 kg)
  - talus_r   mass = 0.27 kg (+217.11% change from original 0.08 kg)
  - calcn_r   mass = 0.75 kg (-29.22% change from original 1.06 kg)
  - toes_r    mass = 0.03 kg (-84.04% change from original 0.18 kg)
  - femur_l   mass = 9.07 kg (+15.46% change from original 7.86 kg)
  - tibia_l   mass = 2.09 kg (-33.14% change from original 3.13 kg)
  - talus_l   mass = 0.27 kg (+217.11% change from original 0.08 kg)
  - calcn_l   mass = 0.75 kg (-29.22% change from original 1.06 kg)
  - toes_l    mass = 0.03 kg (-84.04% change from original 0.18 kg)
  - torso     mass = 21.72 kg (-4.14% change from original 22.66 kg)
  - humerus_r mass = 0.65 kg (-61.91% change from original 1.72 kg)
  - ulna_r    mass = 0.21 kg (-59.71% change from original 0.51 kg)
  - radius_r  mass = 0.21 kg (-59.71% change from original 0.51 kg)
  - hand_r    mass = 0.73 kg (+89.49% change from original 0.39 kg)
  - humerus_l mass = 0.65 kg (-61.91% change from original 1.72 kg)
  - ulna_l    mass = 0.21 kg (-59.71% change from original 0.51 kg)
  - radius_l  mass = 0.21 kg (-59.71% change from original 0.51 kg)
  - hand_l    mass = 0.73 kg (+89.49% change from original 0.39 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: walkingTS4
  - Avg. Marker RMSE      = 1.71 cm
  - Avg. Marker Max Error = 3.92 cm
  - Avg. Residual Force   = 1.38 N
  - Avg. Residual Torque  = 8.08 N-m
  - WARNING: Automatic data processing required modifying TRC data from 2 marker(s)!
  --> See IK/walkingTS4_ik_summary.txt and ID/walkingTS4_id_summary.txt for more details.

trial: walking2
  - Avg. Marker RMSE      = 1.58 cm
  - Avg. Marker Max Error = 3.25 cm
  - Avg. Residual Force   = 1.40 N
  - Avg. Residual Torque  = 5.85 N-m
  - WARNING: Automatic data processing required modifying TRC data from 2 marker(s)!
  --> See IK/walking2_ik_summary.txt and ID/walking2_id_summary.txt for more details.

trial: squatsAsym1
  - Avg. Marker RMSE      = 1.45 cm
  - Avg. Marker Max Error = 3.40 cm
  - Avg. Residual Force   = 3.73 N
  - Avg. Residual Torque  = 5.91 N-m
  --> See IK/squatsAsym1_ik_summary.txt and ID/squatsAsym1_id_summary.txt for more details.

trial: walkingTS3
  - Avg. Marker RMSE      = 1.57 cm
  - Avg. Marker Max Error = 3.87 cm
  - Avg. Residual Force   = 1.36 N
  - Avg. Residual Torque  = 8.55 N-m
  --> See IK/walkingTS3_ik_summary.txt and ID/walkingTS3_id_summary.txt for more details.

trial: squats1
  - Avg. Marker RMSE      = 1.42 cm
  - Avg. Marker Max Error = 3.41 cm
  - Avg. Residual Force   = 9.58 N
  - Avg. Residual Torque  = 4.57 N-m
  --> See IK/squats1_ik_summary.txt and ID/squats1_id_summary.txt for more details.

trial: DJ4
  - Avg. Marker RMSE      = 2.06 cm
  - Avg. Marker Max Error = 5.35 cm
  - Avg. Residual Force   = 154.56 N
  - Avg. Residual Torque  = 69.75 N-m
  - WARNING: 2 marker(s) with RMSE greater than 4 cm!
  --> See IK/DJ4_ik_summary.txt and ID/DJ4_id_summary.txt for more details.

trial: walking3
  - Avg. Marker RMSE      = 1.62 cm
  - Avg. Marker Max Error = 3.41 cm
  - Avg. Residual Force   = 1.33 N
  - Avg. Residual Torque  = 5.71 N-m
  - WARNING: Automatic data processing required modifying TRC data from 2 marker(s)!
  --> See IK/walking3_ik_summary.txt and ID/walking3_id_summary.txt for more details.

trial: walkingTS2
  - Avg. Marker RMSE      = 1.56 cm
  - Avg. Marker Max Error = 3.71 cm
  - Avg. Residual Force   = 1.19 N
  - Avg. Residual Torque  = 6.59 N-m
  --> See IK/walkingTS2_ik_summary.txt and ID/walkingTS2_id_summary.txt for more details.

trial: walking1
  - Avg. Marker RMSE      = 1.59 cm
  - Avg. Marker Max Error = 3.33 cm
  - Avg. Residual Force   = 1.92 N
  - Avg. Residual Torque  = 5.20 N-m
  - WARNING: Automatic data processing required modifying TRC data from 2 marker(s)!
  --> See IK/walking1_ik_summary.txt and ID/walking1_id_summary.txt for more details.


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

 > opensim-cmd run-tool walkingTS4_ik_setup.xml
           # This will create a results file IK/walkingTS4_ik_by_opensim.mot
 > opensim-cmd run-tool walking2_ik_setup.xml
           # This will create a results file IK/walking2_ik_by_opensim.mot
 > opensim-cmd run-tool squatsAsym1_ik_setup.xml
           # This will create a results file IK/squatsAsym1_ik_by_opensim.mot
 > opensim-cmd run-tool walkingTS3_ik_setup.xml
           # This will create a results file IK/walkingTS3_ik_by_opensim.mot
 > opensim-cmd run-tool squats1_ik_setup.xml
           # This will create a results file IK/squats1_ik_by_opensim.mot
 > opensim-cmd run-tool DJ4_ik_setup.xml
           # This will create a results file IK/DJ4_ik_by_opensim.mot
 > opensim-cmd run-tool walking3_ik_setup.xml
           # This will create a results file IK/walking3_ik_by_opensim.mot
 > opensim-cmd run-tool walkingTS2_ik_setup.xml
           # This will create a results file IK/walkingTS2_ik_by_opensim.mot
 > opensim-cmd run-tool walking1_ik_setup.xml
           # This will create a results file IK/walking1_ik_by_opensim.mot


To re-run Inverse Dynamics using OpenSim, you can also use
automatically generated XML configuration files. WARNING: Inverse
Dynamics in OpenSim uses a different time-step definition to the one
used in AddBiomechanics (AddBiomechanics uses semi-implicit Euler,
OpenSim uses splines). This means that your OpenSim inverse dynamics
results WILL NOT MATCH your AddBiomechanics results, and YOU SHOULD
NOT EXPECT THEM TO. The following commands should work (FROM THE "ID"
FOLDER, and not including the leading "> "):

 > opensim-cmd run-tool walkingTS4_id_setup.xml
           # This will create results on time range (0.01s to 1.54s) in file ID/walkingTS4_osim_id.sto
 > opensim-cmd run-tool walking2_id_setup.xml
           # This will create results on time range (0.01s to 1.34s) in file ID/walking2_osim_id.sto
 > opensim-cmd run-tool squatsAsym1_id_setup.xml
           # This will create results on time range (0.01s to 12.78s) in file ID/squatsAsym1_osim_id.sto
 > opensim-cmd run-tool walkingTS3_id_setup.xml
           # This will create results on time range (0.01s to 1.68s) in file ID/walkingTS3_osim_id.sto
 > opensim-cmd run-tool squats1_id_setup.xml
           # This will create results on time range (0.01s to 11.82s) in file ID/squats1_osim_id.sto
 > opensim-cmd run-tool DJ4_id_setup.xml
           # This will create results on time range (1.6s to 2.92s) in file ID/DJ4_osim_id.sto
 > opensim-cmd run-tool walking3_id_setup.xml
           # This will create results on time range (0.01s to 1.36s) in file ID/walking3_osim_id.sto
 > opensim-cmd run-tool walkingTS2_id_setup.xml
           # This will create results on time range (0.01s to 1.79s) in file ID/walkingTS2_osim_id.sto
 > opensim-cmd run-tool walking1_id_setup.xml
           # This will create results on time range (0.01s to 1.3s) in file ID/walking1_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics