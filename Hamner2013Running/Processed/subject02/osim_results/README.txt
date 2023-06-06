*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.49 cm
- Avg. Max Marker Error = 3.68 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 6.16 N
- Avg. Residual Torque = 38.23 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 76.83 kg (+0.46% change from original 76.48 kg)

Individual body mass changes:

  - pelvis    mass = 11.55 kg (-3.57% change from original 11.98 kg)
  - femur_r   mass = 9.83 kg (+3.88% change from original 9.46 kg)
  - tibia_r   mass = 3.77 kg (-0.13% change from original 3.77 kg)
  - talus_r   mass = 0.73 kg (+619.12% change from original 0.10 kg)
  - calcn_r   mass = 1.02 kg (-19.69% change from original 1.27 kg)
  - toes_r    mass = 0.00 kg (-99.45% change from original 0.22 kg)
  - femur_l   mass = 9.83 kg (+3.88% change from original 9.46 kg)
  - tibia_l   mass = 3.77 kg (-0.13% change from original 3.77 kg)
  - talus_l   mass = 0.73 kg (+619.12% change from original 0.10 kg)
  - calcn_l   mass = 1.02 kg (-19.69% change from original 1.27 kg)
  - toes_l    mass = 0.00 kg (-99.45% change from original 0.22 kg)
  - torso     mass = 27.52 kg (+0.83% change from original 27.30 kg)
  - humerus_r mass = 2.20 kg (+6.35% change from original 2.07 kg)
  - ulna_r    mass = 0.56 kg (-9.67% change from original 0.62 kg)
  - radius_r  mass = 0.56 kg (-9.67% change from original 0.62 kg)
  - hand_r    mass = 0.21 kg (-55.57% change from original 0.47 kg)
  - humerus_l mass = 2.20 kg (+6.35% change from original 2.07 kg)
  - ulna_l    mass = 0.56 kg (-9.67% change from original 0.62 kg)
  - radius_l  mass = 0.56 kg (-9.67% change from original 0.62 kg)
  - hand_l    mass = 0.21 kg (-55.57% change from original 0.47 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.57 cm
  - Avg. Marker Max Error = 4.32 cm
  - Avg. Residual Force   = 6.14 N
  - Avg. Residual Torque  = 41.94 N-m
  - WARNING: 1 marker(s) with RMSE greater than 4 cm!
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.25 cm
  - Avg. Marker Max Error = 2.54 cm
  - Avg. Residual Force   = 5.16 N
  - Avg. Residual Torque  = 24.64 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.42 cm
  - Avg. Marker Max Error = 3.24 cm
  - Avg. Residual Force   = 5.94 N
  - Avg. Residual Torque  = 33.67 N-m
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.79 cm
  - Avg. Marker Max Error = 4.90 cm
  - Avg. Residual Force   = 7.67 N
  - Avg. Residual Torque  = 56.21 N-m
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
           # This will create results on time range (0.108333s to 2.208333s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.141667s to 2.55s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (1.141667s to 3.358333s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.175s to 2.116667s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics