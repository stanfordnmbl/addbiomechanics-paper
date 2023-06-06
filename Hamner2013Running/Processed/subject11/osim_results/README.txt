*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.15 cm
- Avg. Max Marker Error = 2.48 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 2.71 N
- Avg. Residual Torque = 30.03 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 71.21 kg (+2.68% change from original 69.35 kg)

Individual body mass changes:

  - pelvis    mass = 12.85 kg (+18.29% change from original 10.87 kg)
  - femur_r   mass = 9.27 kg (+7.98% change from original 8.58 kg)
  - tibia_r   mass = 2.87 kg (-16.14% change from original 3.42 kg)
  - talus_r   mass = 0.24 kg (+158.64% change from original 0.09 kg)
  - calcn_r   mass = 0.21 kg (-81.58% change from original 1.15 kg)
  - toes_r    mass = 0.26 kg (+28.78% change from original 0.20 kg)
  - femur_l   mass = 9.27 kg (+7.98% change from original 8.58 kg)
  - tibia_l   mass = 2.87 kg (-16.14% change from original 3.42 kg)
  - talus_l   mass = 0.24 kg (+158.64% change from original 0.09 kg)
  - calcn_l   mass = 0.21 kg (-81.58% change from original 1.15 kg)
  - toes_l    mass = 0.26 kg (+28.78% change from original 0.20 kg)
  - torso     mass = 26.59 kg (+7.44% change from original 24.75 kg)
  - humerus_r mass = 1.66 kg (-11.28% change from original 1.88 kg)
  - ulna_r    mass = 0.32 kg (-43.71% change from original 0.56 kg)
  - radius_r  mass = 0.32 kg (-43.71% change from original 0.56 kg)
  - hand_r    mass = 0.74 kg (+76.21% change from original 0.42 kg)
  - humerus_l mass = 1.66 kg (-11.28% change from original 1.88 kg)
  - ulna_l    mass = 0.32 kg (-43.71% change from original 0.56 kg)
  - radius_l  mass = 0.32 kg (-43.71% change from original 0.56 kg)
  - hand_l    mass = 0.74 kg (+76.21% change from original 0.42 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.18 cm
  - Avg. Marker Max Error = 2.43 cm
  - Avg. Residual Force   = 2.40 N
  - Avg. Residual Torque  = 27.43 N-m
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.03 cm
  - Avg. Marker Max Error = 2.22 cm
  - Avg. Residual Force   = 2.34 N
  - Avg. Residual Torque  = 20.74 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.13 cm
  - Avg. Marker Max Error = 2.44 cm
  - Avg. Residual Force   = 3.00 N
  - Avg. Residual Torque  = 26.41 N-m
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.30 cm
  - Avg. Marker Max Error = 2.90 cm
  - Avg. Residual Force   = 3.19 N
  - Avg. Residual Torque  = 49.28 N-m
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
           # This will create results on time range (0.55s to 2.39s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (1.42s to 3.58s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.44s to 2.44s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.14s to 1.8s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics