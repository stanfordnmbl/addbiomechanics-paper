*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 0.55 cm
- Avg. Max Marker Error = 1.31 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 0.01 N
- Avg. Residual Torque = 0.00 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 80.25 kg (-0.06% change from original 80.3 kg)

Individual body mass changes:

  - pelvis    mass = 11.43 kg (-0.20% change from original 11.45 kg)
  - femur_r   mass = 9.05 kg (+0.01% change from original 9.05 kg)
  - tibia_r   mass = 3.63 kg (+0.69% change from original 3.61 kg)
  - talus_r   mass = 0.12 kg (+24.44% change from original 0.10 kg)
  - calcn_r   mass = 1.23 kg (+1.17% change from original 1.22 kg)
  - toes_r    mass = 0.20 kg (-4.86% change from original 0.21 kg)
  - femur_l   mass = 9.05 kg (+0.01% change from original 9.05 kg)
  - tibia_l   mass = 3.63 kg (+0.69% change from original 3.61 kg)
  - talus_l   mass = 0.12 kg (+24.44% change from original 0.10 kg)
  - calcn_l   mass = 1.23 kg (+1.17% change from original 1.22 kg)
  - toes_l    mass = 0.20 kg (-4.86% change from original 0.21 kg)
  - torso     mass = 33.25 kg (-0.13% change from original 33.29 kg)
  - humerus_r mass = 1.96 kg (-0.75% change from original 1.98 kg)
  - ulna_r    mass = 0.58 kg (-1.27% change from original 0.59 kg)
  - radius_r  mass = 0.58 kg (-1.27% change from original 0.59 kg)
  - hand_r    mass = 0.43 kg (-3.21% change from original 0.44 kg)
  - humerus_l mass = 1.96 kg (-0.75% change from original 1.98 kg)
  - ulna_l    mass = 0.58 kg (-1.27% change from original 0.59 kg)
  - radius_l  mass = 0.58 kg (-1.27% change from original 0.59 kg)
  - hand_l    mass = 0.43 kg (-3.21% change from original 0.44 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: walk2
  - Avg. Marker RMSE      = 0.55 cm
  - Avg. Marker Max Error = 1.31 cm
  - Avg. Residual Force   = 0.01 N
  - Avg. Residual Torque  = 0.00 N-m
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
           # This will create results on time range (1.415s to 2.515s) in file ID/walk2_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics