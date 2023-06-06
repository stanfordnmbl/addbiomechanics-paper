*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.66 cm
- Avg. Max Marker Error = 4.06 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 5.32 N
- Avg. Residual Torque = 34.00 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 68.45 kg (+1.89% change from original 67.18 kg)

Individual body mass changes:

  - pelvis    mass = 12.39 kg (+17.69% change from original 10.53 kg)
  - femur_r   mass = 8.72 kg (+4.90% change from original 8.31 kg)
  - tibia_r   mass = 2.51 kg (-24.23% change from original 3.31 kg)
  - talus_r   mass = 0.30 kg (+230.37% change from original 0.09 kg)
  - calcn_r   mass = 0.87 kg (-21.88% change from original 1.12 kg)
  - toes_r    mass = 0.14 kg (-27.09% change from original 0.19 kg)
  - femur_l   mass = 8.72 kg (+4.90% change from original 8.31 kg)
  - tibia_l   mass = 2.51 kg (-24.23% change from original 3.31 kg)
  - talus_l   mass = 0.30 kg (+230.37% change from original 0.09 kg)
  - calcn_l   mass = 0.87 kg (-21.88% change from original 1.12 kg)
  - toes_l    mass = 0.14 kg (-27.09% change from original 0.19 kg)
  - torso     mass = 25.18 kg (+5.04% change from original 23.98 kg)
  - humerus_r mass = 1.30 kg (-28.71% change from original 1.82 kg)
  - ulna_r    mass = 0.30 kg (-44.56% change from original 0.54 kg)
  - radius_r  mass = 0.30 kg (-44.56% change from original 0.54 kg)
  - hand_r    mass = 1.00 kg (+144.71% change from original 0.41 kg)
  - humerus_l mass = 1.30 kg (-28.71% change from original 1.82 kg)
  - ulna_l    mass = 0.30 kg (-44.56% change from original 0.54 kg)
  - radius_l  mass = 0.30 kg (-44.56% change from original 0.54 kg)
  - hand_l    mass = 1.00 kg (+144.71% change from original 0.41 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.68 cm
  - Avg. Marker Max Error = 3.82 cm
  - Avg. Residual Force   = 5.13 N
  - Avg. Residual Torque  = 37.75 N-m
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.62 cm
  - Avg. Marker Max Error = 4.16 cm
  - Avg. Residual Force   = 5.77 N
  - Avg. Residual Torque  = 19.32 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.63 cm
  - Avg. Marker Max Error = 4.14 cm
  - Avg. Residual Force   = 5.09 N
  - Avg. Residual Torque  = 23.84 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.72 cm
  - Avg. Marker Max Error = 4.10 cm
  - Avg. Residual Force   = 5.27 N
  - Avg. Residual Torque  = 58.01 N-m
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
           # This will create results on time range (0.091667s to 2.0s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.241667s to 2.258333s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.175s to 2.166667s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.108333s to 1.883333s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics