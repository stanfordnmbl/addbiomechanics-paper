*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.69 cm
- Avg. Max Marker Error = 4.48 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 5.96 N
- Avg. Residual Torque = 41.16 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 81.29 kg (+1.02% change from original 80.47 kg)

Individual body mass changes:

  - pelvis    mass = 13.21 kg (+4.80% change from original 12.61 kg)
  - femur_r   mass = 10.52 kg (+5.60% change from original 9.96 kg)
  - tibia_r   mass = 4.14 kg (+4.23% change from original 3.97 kg)
  - talus_r   mass = 0.61 kg (+467.45% change from original 0.11 kg)
  - calcn_r   mass = 1.28 kg (-4.27% change from original 1.34 kg)
  - toes_r    mass = 0.11 kg (-51.95% change from original 0.23 kg)
  - femur_l   mass = 10.52 kg (+5.60% change from original 9.96 kg)
  - tibia_l   mass = 4.14 kg (+4.23% change from original 3.97 kg)
  - talus_l   mass = 0.61 kg (+467.45% change from original 0.11 kg)
  - calcn_l   mass = 1.28 kg (-4.27% change from original 1.34 kg)
  - toes_l    mass = 0.11 kg (-51.95% change from original 0.23 kg)
  - torso     mass = 29.89 kg (+4.07% change from original 28.72 kg)
  - humerus_r mass = 1.75 kg (-19.72% change from original 2.18 kg)
  - ulna_r    mass = 0.26 kg (-59.90% change from original 0.65 kg)
  - radius_r  mass = 0.26 kg (-59.90% change from original 0.65 kg)
  - hand_r    mass = 0.17 kg (-64.68% change from original 0.49 kg)
  - humerus_l mass = 1.75 kg (-19.72% change from original 2.18 kg)
  - ulna_l    mass = 0.26 kg (-59.90% change from original 0.65 kg)
  - radius_l  mass = 0.26 kg (-59.90% change from original 0.65 kg)
  - hand_l    mass = 0.17 kg (-64.68% change from original 0.49 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.86 cm
  - Avg. Marker Max Error = 4.88 cm
  - Avg. Residual Force   = 5.50 N
  - Avg. Residual Torque  = 56.76 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.47 cm
  - Avg. Marker Max Error = 3.67 cm
  - Avg. Residual Force   = 5.98 N
  - Avg. Residual Torque  = 18.21 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.65 cm
  - Avg. Marker Max Error = 4.32 cm
  - Avg. Residual Force   = 7.44 N
  - Avg. Residual Torque  = 33.47 N-m
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.81 cm
  - Avg. Marker Max Error = 5.26 cm
  - Avg. Residual Force   = 4.64 N
  - Avg. Residual Torque  = 62.05 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
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
           # This will create results on time range (0.66s to 2.72s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.84s to 3.18s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.62s to 2.84s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.27s to 2.11s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics