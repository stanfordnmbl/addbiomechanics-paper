*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 0.73 cm
- Avg. Max Marker Error = 1.74 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 0.05 N
- Avg. Residual Torque = 0.07 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 68.46 kg (-0.07% change from original 68.5 kg)

Individual body mass changes:

  - pelvis    mass = 9.73 kg (-0.39% change from original 9.77 kg)
  - femur_r   mass = 7.71 kg (-0.07% change from original 7.72 kg)
  - tibia_r   mass = 3.11 kg (+1.28% change from original 3.08 kg)
  - talus_r   mass = 0.15 kg (+85.87% change from original 0.08 kg)
  - calcn_r   mass = 1.08 kg (+4.16% change from original 1.04 kg)
  - toes_r    mass = 0.15 kg (-15.73% change from original 0.18 kg)
  - femur_l   mass = 7.71 kg (-0.07% change from original 7.72 kg)
  - tibia_l   mass = 3.11 kg (+1.28% change from original 3.08 kg)
  - talus_l   mass = 0.15 kg (+85.87% change from original 0.08 kg)
  - calcn_l   mass = 1.08 kg (+4.16% change from original 1.04 kg)
  - toes_l    mass = 0.15 kg (-15.73% change from original 0.18 kg)
  - torso     mass = 28.34 kg (-0.20% change from original 28.40 kg)
  - humerus_r mass = 1.68 kg (-0.33% change from original 1.69 kg)
  - ulna_r    mass = 0.49 kg (-2.08% change from original 0.50 kg)
  - radius_r  mass = 0.49 kg (-2.08% change from original 0.50 kg)
  - hand_r    mass = 0.31 kg (-17.87% change from original 0.38 kg)
  - humerus_l mass = 1.68 kg (-0.33% change from original 1.69 kg)
  - ulna_l    mass = 0.49 kg (-2.08% change from original 0.50 kg)
  - radius_l  mass = 0.49 kg (-2.08% change from original 0.50 kg)
  - hand_l    mass = 0.31 kg (-17.87% change from original 0.38 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: walk2
  - Avg. Marker RMSE      = 0.73 cm
  - Avg. Marker Max Error = 1.74 cm
  - Avg. Residual Force   = 0.05 N
  - Avg. Residual Torque  = 0.07 N-m
  --> See IK/walk2_ik_summary.txt and ID/walk2_id_summary.txt for more details.


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

 > opensim-cmd run-tool walk2_ik_setup.xml
           # This will create a results file IK/walk2_ik_by_opensim.mot


To re-run Inverse Dynamics using OpenSim, you can also use
automatically generated XML configuration files. WARNING: Inverse
Dynamics in OpenSim uses a different time-step definition to the one
used in AddBiomechanics (AddBiomechanics uses semi-implicit Euler,
OpenSim uses splines). This means that your OpenSim inverse dynamics
results WILL NOT MATCH your AddBiomechanics results, and YOU SHOULD
NOT EXPECT THEM TO. The following commands should work (FROM THE "ID"
FOLDER, and not including the leading "> "):

 > opensim-cmd run-tool walk2_id_setup.xml
           # This will create results on time range (2.725s to 3.774999999999999s) in file ID/walk2_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics