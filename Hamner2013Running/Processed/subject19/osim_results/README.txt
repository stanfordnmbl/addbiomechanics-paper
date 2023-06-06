*** This data was generated with AddBiomechanics (www.addbiomechanics.org) ***
AddBiomechanics was written by Keenon Werling.

Automatic processing achieved the following marker errors (averaged
over all frames of all trials):

- Avg. Marker RMSE      = 1.62 cm
- Avg. Max Marker Error = 4.18 cm

Automatic processing reduced the residual loads needed for dynamic
consistency to the following magnitudes (averaged over all frames of
all trials):

- Avg. Residual Force  = 4.83 N
- Avg. Residual Torque = 32.43 N-m

Automatic processing found a new model mass to achieve dynamic
consistency:

  - Total mass = 66.24 kg (+1.69% change from original 65.14 kg)

Individual body mass changes:

  - pelvis    mass = 10.90 kg (+6.78% change from original 10.21 kg)
  - femur_r   mass = 8.70 kg (+7.88% change from original 8.06 kg)
  - tibia_r   mass = 3.17 kg (-1.20% change from original 3.21 kg)
  - talus_r   mass = 0.33 kg (+279.09% change from original 0.09 kg)
  - calcn_r   mass = 1.26 kg (+16.57% change from original 1.08 kg)
  - toes_r    mass = 0.00 kg (-98.64% change from original 0.19 kg)
  - femur_l   mass = 8.70 kg (+7.88% change from original 8.06 kg)
  - tibia_l   mass = 3.17 kg (-1.20% change from original 3.21 kg)
  - talus_l   mass = 0.33 kg (+279.09% change from original 0.09 kg)
  - calcn_l   mass = 1.26 kg (+16.57% change from original 1.08 kg)
  - toes_l    mass = 0.00 kg (-98.64% change from original 0.19 kg)
  - torso     mass = 24.70 kg (+6.23% change from original 23.25 kg)
  - humerus_r mass = 0.69 kg (-60.67% change from original 1.76 kg)
  - ulna_r    mass = 0.41 kg (-22.40% change from original 0.53 kg)
  - radius_r  mass = 0.41 kg (-22.40% change from original 0.53 kg)
  - hand_r    mass = 0.35 kg (-12.15% change from original 0.40 kg)
  - humerus_l mass = 0.69 kg (-60.67% change from original 1.76 kg)
  - ulna_l    mass = 0.41 kg (-22.40% change from original 0.53 kg)
  - radius_l  mass = 0.41 kg (-22.40% change from original 0.53 kg)
  - hand_l    mass = 0.35 kg (-12.15% change from original 0.40 kg)

The following trials were processed to perform automatic body scaling,
marker registration, and residual reduction:

trial: run400
  - Avg. Marker RMSE      = 1.62 cm
  - Avg. Marker Max Error = 4.07 cm
  - Avg. Residual Force   = 3.63 N
  - Avg. Residual Torque  = 35.23 N-m
  --> See IK/run400_ik_summary.txt and ID/run400_id_summary.txt for more details.

trial: run200
  - Avg. Marker RMSE      = 1.49 cm
  - Avg. Marker Max Error = 3.76 cm
  - Avg. Residual Force   = 7.14 N
  - Avg. Residual Torque  = 20.59 N-m
  --> See IK/run200_ik_summary.txt and ID/run200_id_summary.txt for more details.

trial: run300
  - Avg. Marker RMSE      = 1.55 cm
  - Avg. Marker Max Error = 3.97 cm
  - Avg. Residual Force   = 3.42 N
  - Avg. Residual Torque  = 28.03 N-m
  --> See IK/run300_ik_summary.txt and ID/run300_id_summary.txt for more details.

trial: run500
  - Avg. Marker RMSE      = 1.87 cm
  - Avg. Marker Max Error = 5.02 cm
  - Avg. Residual Force   = 4.98 N
  - Avg. Residual Torque  = 48.41 N-m
  - WARNING: 2 marker(s) with RMSE greater than 4 cm!
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
           # This will create results on time range (0.65s to 2.658333s) in file ID/run400_osim_id.sto
 > opensim-cmd run-tool run200_id_setup.xml
           # This will create results on time range (0.175s to 2.433333s) in file ID/run200_osim_id.sto
 > opensim-cmd run-tool run300_id_setup.xml
           # This will create results on time range (0.158333s to 2.308333s) in file ID/run300_osim_id.sto
 > opensim-cmd run-tool run500_id_setup.xml
           # This will create results on time range (0.2s to 2.108333s) in file ID/run500_osim_id.sto


The original unscaled model file is present in:

Models/unscaled_generic.osim

There is also an unscaled model, with markers moved to spots found by
this tool, at:

Models/unscaled_but_with_optimized_markers.osim

If you encounter errors, please submit a post to the AddBiomechanics
user forum on SimTK.org :

   https://simtk.org/projects/addbiomechanics