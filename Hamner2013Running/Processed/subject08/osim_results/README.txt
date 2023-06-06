*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.60 cm
- Avg. Max Marker Error = 3.53 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 6.91 N
- Avg. Residual Torque = 31.03 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 81.24 kg (-1.37% change from original 82.37 kg)

Individual body mass changes:

  - pelvis    mass = 13.27 kg (+2.80% change from original 12.91 kg)
  - femur_r   mass = 10.10 kg (-0.94% change from original 10.19 kg)
  - tibia_r   mass = 3.45 kg (-14.97% change from original 4.06 kg)
  - talus_r   mass = 0.30 kg (+171.18% change from original 0.11 kg)
  - calcn_r   mass = 1.34 kg (-1.85% change from original 1.37 kg)
  - toes_r    mass = 0.14 kg (-40.24% change from original 0.24 kg)
  - femur_l   mass = 10.10 kg (-0.94% change from original 10.19 kg)
  - tibia_l   mass = 3.45 kg (-14.97% change from original 4.06 kg)
  - talus_l   mass = 0.30 kg (+171.18% change from original 0.11 kg)
  - calcn_l   mass = 1.34 kg (-1.85% change from original 1.37 kg)
  - toes_l    mass = 0.14 kg (-40.24% change from original 0.24 kg)
  - torso     mass = 29.34 kg (-0.20% change from original 29.40 kg)
  - humerus_r mass = 2.05 kg (-7.81% change from original 2.23 kg)
  - ulna_r    mass = 0.47 kg (-29.72% change from original 0.67 kg)
  - radius_r  mass = 0.47 kg (-29.72% change from original 0.67 kg)
  - hand_r    mass = 0.99 kg (+98.25% change from original 0.50 kg)
  - humerus_l mass = 2.05 kg (-7.81% change from original 2.23 kg)
  - ulna_l    mass = 0.47 kg (-29.72% change from original 0.67 kg)
  - radius_l  mass = 0.47 kg (-29.72% change from original 0.67 kg)
  - hand_l    mass = 0.99 kg (+98.25% change from original 0.50 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.61 cm
  - Avg. Marker Max Error = 3.57 cm
  - Avg. Residual Force   = 8.05 N
  - Avg. Residual Torque  = 34.12 N-m
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.49 cm
  - Avg. Marker Max Error = 3.20 cm
  - Avg. Residual Force   = 7.12 N
  - Avg. Residual Torque  = 18.21 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.56 cm
  - Avg. Marker Max Error = 3.56 cm
  - Avg. Residual Force   = 6.62 N
  - Avg. Residual Torque  = 24.45 N-m
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.78 cm
  - Avg. Marker Max Error = 3.86 cm
  - Avg. Residual Force   = 5.78 N
  - Avg. Residual Torque  = 49.86 N-m
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
           # This will create results on time range (0.2s to 2.13s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.82s to 2.94s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.44s to 2.41s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.4s to 2.21s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics