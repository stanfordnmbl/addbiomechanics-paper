import os
import opensim as osim
import numpy as np
import copy

forceNamesRightFoot = ['forceset/contactHeel_r',
                       'forceset/contactLateralRearfoot_r',
                       'forceset/contactLateralMidfoot_r',
                       'forceset/contactLateralToe_r',
                       'forceset/contactMedialToe_r',
                       'forceset/contactMedialMidfoot_r']
forceNamesLeftFoot = ['forceset/contactHeel_l',
                      'forceset/contactLateralRearfoot_l',
                      'forceset/contactLateralMidfoot_l',
                      'forceset/contactLateralToe_l',
                      'forceset/contactMedialToe_l',
                      'forceset/contactMedialMidfoot_l']


def create_model_processor(model_fpath, external_loads_fpath=None, remove_forces=False, lock_toes=False,
                           weld_toes=False, weld_wrist=False):

    osim.Logger.setLevelString('error')

    # Load model
    # ----------
    model = osim.Model(model_fpath)
    state = model.initSystem()
    mass = model.getTotalMass(state)

    # Remove the contact force elements
    # ---------------------------------
    if external_loads_fpath is not None:
        forceSet = model.updForceSet()
        for forceName in forceNamesRightFoot + forceNamesLeftFoot:
            print(forceName)
            forceSet.remove(forceSet.getIndex(forceName[9:]))

        contactGeometrySet = model.updContactGeometrySet()
        contactGeometrySet.clearAndDestroy()

    coordSet = model.updCoordinateSet()
    for coordName in ['mtp_angle']:
        for side in ['_l', '_r']:
            coord = coordSet.get(f'{coordName}{side}')
            if lock_toes:
                coord.set_locked(True)
            else:
                coord.set_locked(False)

    # Arm actuators
    coordNames = ['arm_flex', 'arm_add', 'arm_rot', 
                  'elbow_flex', 'pro_sup']
    strengths = [0.5, 0.5, 0.5, 0.2, 0.2]
    for coordName, strength in zip(coordNames, strengths):
        for side in ['_l', '_r']:
            actu = osim.ActivationCoordinateActuator()
            actu.set_coordinate(f'{coordName}{side}')
            actu.setName(f'torque_{coordName}{side}')
            actu.setOptimalForce(strength*mass)
            actu.setMinControl(-1.0)
            actu.setMaxControl(1.0)
            model.addForce(actu)

    # Lumbar actuators
    coordNames = ['lumbar_extension', 
                  'lumbar_bending', 
                  'lumbar_rotation']
    for coordName in coordNames:
        actu = osim.ActivationCoordinateActuator()
        actu.set_coordinate(coordName)
        actu.setName(f'torque_{coordName}')
        actu.setOptimalForce(mass)
        actu.setMinControl(-1.0)
        actu.setMaxControl(1.0)
        model.addForce(actu)

    stiffnesses = [1.0, 1.5, 0.5] # N-m/rad*kg
    for coordName, stiffness in zip(coordNames, stiffnesses):
        sgf = osim.SpringGeneralizedForce(coordName)
        sgf.setName(f'passive_stiffness_{coordName}')
        sgf.setStiffness(stiffness * mass)
        sgf.setViscosity(2.0)
        model.addForce(sgf)

    model.finalizeConnections()

    if weld_toes:
        forceSet = model.updForceSet()
        for side in ['_l', '_r']:
            forceSet.remove(forceSet.getIndex(f'PassiveToeDamping{side}'))
        model.finalizeConnections()

    modelProcessor = osim.ModelProcessor(model)
    jointsToWeld = list()
    for side in ['_l', '_r']:
        if weld_wrist:
            jointsToWeld.append(f'radius_hand{side}')
        if weld_toes:
            jointsToWeld.append(f'mtp{side}')
    modelProcessor.append(osim.ModOpReplaceJointsWithWelds(jointsToWeld))
    modelProcessor.append(osim.ModOpReplaceMusclesWithDeGrooteFregly2016())
    modelProcessor.append(osim.ModOpIgnoreTendonCompliance())
    modelProcessor.append(osim.ModOpFiberDampingDGF(0.01))
    if external_loads_fpath is not None:
        modelProcessor.append(osim.ModOpAddExternalLoads(external_loads_fpath))

    # Enable tendon compliance for the ankle plantarflexors.
    # ------------------------------------------------------
    model = modelProcessor.process()
    model.initSystem()
    muscles = model.updMuscles()
    for imusc in np.arange(muscles.getSize()):
        muscle = osim.DeGrooteFregly2016Muscle.safeDownCast(muscles.get(int(imusc)))
        muscName = muscle.getName()

        if ('gas' in muscName) or ('soleus' in muscName):
            muscle.set_ignore_tendon_compliance(False)
            muscle.set_tendon_strain_at_one_norm_force(0.10)
            muscle.set_passive_fiber_strain_at_one_norm_force(2.0)

    # Remove the forces
    # -----------------
    if remove_forces:
        forceSet = model.updForceSet()
        forceSet.clearAndDestroy()
        contactGeometrySet = model.updContactGeometrySet()
        contactGeometrySet.clearAndDestroy()

    model.finalizeFromProperties()
    model.finalizeConnections()
    modelProcessor = osim.ModelProcessor(model)
    osim.Logger.setLevelString('info')

    return modelProcessor


def run_timestepping_problem(subject, model_fpath, external_loads_fpath, unperturbed_fpath):

    # Create the model
    # ----------------
    modelProcessor = create_model_processor(model_fpath, external_loads_fpath)
    model = modelProcessor.process()
    model.initSystem()

    # Load the unperturbed walking trajectory
    # ---------------------------------------
    trajectory = osim.MocoTrajectory(unperturbed_fpath)

    # Add the PrescribedController to the model
    # -----------------------------------------
    osim.prescribeControlsToModel(trajectory, model, 'PiecewiseLinearFunction')

    # Add states reporter to the model.
    # ---------------------------------
    statesRep = osim.StatesTrajectoryReporter()
    statesRep.setName('states_reporter')
    statesRep.set_report_time_interval(5e-3)
    model.addComponent(statesRep)

    # Simulate!
    # ---------
    time = trajectory.getTime()
    model.initSystem()
    manager = osim.Manager(model)
    manager.setIntegratorAccuracy(1e-6)
    manager.setIntegratorMinimumStepSize(1e-6)
    manager.setIntegratorMaximumStepSize(1e-2)
    statesTraj = trajectory.exportToStatesTrajectory(model)
    manager.initialize(statesTraj.get(0))
    manager.integrate(time[time.size() - 150])

    # Export results from states reporter to a table.
    # -----------------------------------------------
    statesTrajRep = osim.StatesTrajectoryReporter().safeDownCast(
        model.getComponent('/states_reporter'))
    states = statesTrajRep.getStates().exportToTable(model)
    controls = trajectory.exportToControlsTable()

    return states


def create_external_loads_table_for_gait(model, solution_fpath):
    model.initSystem()
    externalForcesTable = osim.TimeSeriesTableVec3()
    solution = osim.MocoTrajectory(solution_fpath)
    statesTrajectory = solution.exportToStatesTrajectory(model)
    numStates = statesTrajectory.getSize()

    for istate in range(numStates):

        state = statesTrajectory.get(istate)
        model.realizeVelocity(state)

        sphereForcesRight = osim.Vec3(0)
        sphereTorquesRight = osim.Vec3(0)
        halfSpaceForcesRight = osim.Vec3(0)
        halfSpaceTorquesRight = osim.Vec3(0)
        # Loop through all Forces of the right side.
        for smoothForce in forceNamesRightFoot:
            force = osim.Force.safeDownCast(model.getComponent(smoothForce))
            forceValues = force.getRecordValues(state)
            sphereForcesRight[0] += forceValues.get(0)
            sphereForcesRight[1] += forceValues.get(1)
            sphereForcesRight[2] += forceValues.get(2)
            sphereTorquesRight[0] += forceValues.get(3)
            sphereTorquesRight[1] += forceValues.get(4)
            sphereTorquesRight[2] += forceValues.get(5)
            halfSpaceForcesRight[0] += forceValues.get(6)
            halfSpaceForcesRight[1] += forceValues.get(7)
            halfSpaceForcesRight[2] += forceValues.get(8)
            halfSpaceTorquesRight[0] += forceValues.get(9)
            halfSpaceTorquesRight[1] += forceValues.get(10)
            halfSpaceTorquesRight[2] += forceValues.get(11)

        # Loop through all Forces of the left side.
        sphereForcesLeft = osim.Vec3(0)
        sphereTorquesLeft = osim.Vec3(0)
        halfSpaceForcesLeft = osim.Vec3(0)
        halfSpaceTorquesLeft = osim.Vec3(0)
        for smoothForce in forceNamesLeftFoot:
            force = osim.Force.safeDownCast(model.getComponent(smoothForce))
            forceValues = force.getRecordValues(state)
            sphereForcesLeft[0] += forceValues.get(0)
            sphereForcesLeft[1] += forceValues.get(1)
            sphereForcesLeft[2] += forceValues.get(2)
            sphereTorquesLeft[0] += forceValues.get(3)
            sphereTorquesLeft[1] += forceValues.get(4)
            sphereTorquesLeft[2] += forceValues.get(5)
            halfSpaceForcesLeft[0] += forceValues.get(6)
            halfSpaceForcesLeft[1] += forceValues.get(7)
            halfSpaceForcesLeft[2] += forceValues.get(8)
            halfSpaceTorquesLeft[0] += forceValues.get(9)
            halfSpaceTorquesLeft[1] += forceValues.get(10)
            halfSpaceTorquesLeft[2] += forceValues.get(11)

        # Compute center of pressure (CoP) for each foot.
        copRight = osim.Vec3(0)
        copLeft = osim.Vec3(0)
        copRight[0] = halfSpaceTorquesRight[2] / halfSpaceForcesRight[1]
        copRight[2] = -halfSpaceTorquesRight[0] / halfSpaceForcesRight[1]
        copLeft[0] = halfSpaceTorquesLeft[2] / halfSpaceForcesLeft[1]
        copLeft[2] = -halfSpaceTorquesLeft[0] / halfSpaceForcesLeft[1]

        # Compute torques for each foot.
        torquesRight = osim.Vec3(0)
        torquesLeft = osim.Vec3(0)
        torquesRight[1] = -halfSpaceTorquesRight[1] + copRight[2]*halfSpaceForcesRight[0] - copRight[0]*halfSpaceForcesRight[2]
        torquesLeft[1] = -halfSpaceTorquesLeft[1] + copLeft[2]*halfSpaceForcesLeft[0] - copLeft[0]*halfSpaceForcesLeft[2]

        # Append row to table.
        row = osim.RowVectorVec3(6)
        row[0] = sphereForcesRight
        row[1] = copRight
        row[2] = sphereForcesLeft
        row[3] = copLeft
        row[4] = torquesRight
        row[5] = torquesLeft
        externalForcesTable.appendRow(state.getTime(), row)

    # Create table.
    labels = osim.StdVectorString()
    labels.append('ground_force_r_v')
    labels.append('ground_force_r_p')
    labels.append('ground_force_l_v')
    labels.append('ground_force_l_p')
    labels.append('ground_torque_r_')
    labels.append('ground_torque_l_')

    externalForcesTable.setColumnLabels(labels)

    suffixes = osim.StdVectorString()
    suffixes.append('x')
    suffixes.append('y')
    suffixes.append('z')

    return externalForcesTable.flatten(suffixes)


def create_contact_sphere_force_table(model, solution_fpath):
    model.initSystem()
    externalForcesTable = osim.TimeSeriesTableVec3()
    solution = osim.MocoTrajectory(solution_fpath)
    statesTrajectory = solution.exportToStatesTrajectory(model)
    numStates = statesTrajectory.getSize()

    forceNames = ['forceset/contactHeel',
                  'forceset/contactLateralRearfoot',
                  'forceset/contactLateralMidfoot',
                  'forceset/contactLateralToe',
                  'forceset/contactMedialToe',
                  'forceset/contactMedialMidfoot'
                  ]

    forceLabels = ['heel',
                   'lat_rear',
                   'lat_mid',
                   'lat_toe',
                   'med_toe',
                   'med_mid',
                   ]

    sphereNames = ['contactgeometryset/heel',
                   'contactgeometryset/lateralRearfoot',
                   'contactgeometryset/lateralMidfoot',
                   'contactgeometryset/lateralToe',
                   'contactgeometryset/medialToe',
                   'contactgeometryset/medialMidfoot',
                   ]

    for istate in range(numStates):
        state = statesTrajectory.get(istate)
        model.realizeVelocity(state)
        row = osim.RowVectorVec3(3 * 2 * len(forceNames))

        for iside, side in enumerate(['_r', '_l']):
            offset = 3 * iside * len(sphereNames)
            zipped = zip(forceNames, forceLabels, sphereNames)

            for i, (forceName, forceLabel, sphereName) in enumerate(zipped):
                force = osim.Vec3(0)
                torque = osim.Vec3(0)

                forceObj = osim.Force.safeDownCast(
                    model.getComponent(f'{forceName}{side}'))
                forceValues = forceObj.getRecordValues(state)

                force[0] = forceValues.get(0)
                force[1] = forceValues.get(1)
                force[2] = forceValues.get(2)
                torque[0] = forceValues.get(3)
                torque[1] = forceValues.get(4)
                torque[2] = forceValues.get(5)

                sphere = osim.ContactSphere.safeDownCast(
                    model.getComponent(f'{sphereName}{side}'))
                frame = sphere.getFrame()
                position = frame.getPositionInGround(state)

                row[3 * i + offset] = force
                row[3 * i + 1 + offset] = position
                row[3 * i + 2 + offset] = torque

        externalForcesTable.appendRow(state.getTime(), row)

    labels = osim.StdVectorString()
    for side in ['_r', '_l']:
        for forceLabel in forceLabels:
            for suffix in ['_force_v', '_force_p', '_torque_']:
                labels.append(f'{forceLabel}{side}{suffix}')
    externalForcesTable.setColumnLabels(labels)

    suffixes = osim.StdVectorString()
    suffixes.append('x')
    suffixes.append('y')
    suffixes.append('z')

    return externalForcesTable.flatten(suffixes)


def apply_generic_marker_offsets_to_model(generic_model, scaled_model, scaled_reregistered_model):

    generic = osim.Model(generic_model)
    generic.initSystem()
    scaled = osim.Model(scaled_model)
    scaled.initSystem()

    generic_markers = generic.getMarkerSet()
    scaled_markers = scaled.updMarkerSet()
    generic_bodyset = generic.getBodySet()
    scaled_bodyset = scaled.getBodySet()

    for imarker in range(generic_markers.getSize()):
        generic_marker = generic_markers.get(imarker)
        generic_marker_name = generic_marker.getName()
        generic_body_name = generic_marker.getParentFrameName()
        generic_body = generic_bodyset.get(generic_body_name[9:])
        generic_geo0 = generic_body.get_attached_geometry(0)
        generic_scale_factors = generic_geo0.get_scale_factors()

        scaled_marker = scaled_markers.get(generic_marker.getName())
        scaled_body_name = scaled_marker.getParentFrameName()
        scaled_body = scaled_bodyset.get(scaled_body_name[9:])
        scaled_geo0 = scaled_body.get_attached_geometry(0)
        scaled_scale_factors = scaled_geo0.get_scale_factors()

        x_scale = scaled_scale_factors.get(0) / generic_scale_factors.get(0)
        y_scale = scaled_scale_factors.get(1) / generic_scale_factors.get(1)
        z_scale = scaled_scale_factors.get(2) / generic_scale_factors.get(2)

        generic_marker_offset = generic_marker.get_location()
        generic_marker_offset[0] *= x_scale
        generic_marker_offset[1] *= y_scale
        generic_marker_offset[2] *= z_scale

        scaled_marker = scaled_markers.get(generic_marker_name)
        scaled_marker.set_location(generic_marker_offset)

    scaled.finalizeFromProperties()
    scaled.initSystem()
    scaled.printToXML(scaled_reregistered_model)


def get_markers_list():

    includedMarkers = list()
    includedMarkers.append('CLAV')
    includedMarkers.append('C7')
    for side in ['R', 'L']:
        includedMarkers.append(f'{side}ACR')
        includedMarkers.append(f'{side}ASH')
        includedMarkers.append(f'{side}PSH')
        includedMarkers.append(f'{side}LEL')
        includedMarkers.append(f'{side}MEL')
        includedMarkers.append(f'{side}UA1')
        includedMarkers.append(f'{side}UA2')
        includedMarkers.append(f'{side}UA3')
        includedMarkers.append(f'{side}FAsuperior')
        includedMarkers.append(f'{side}FAradius')
        includedMarkers.append(f'{side}FAulna')
        includedMarkers.append(f'{side}ASI')
        includedMarkers.append(f'{side}PSI')
        includedMarkers.append(f'{side}CAL')
        includedMarkers.append(f'{side}TOE')
        includedMarkers.append(f'{side}MT5')
        includedMarkers.append(f'{side}TH1')
        includedMarkers.append(f'{side}TH2')
        includedMarkers.append(f'{side}TH3')
        includedMarkers.append(f'{side}TB1')
        includedMarkers.append(f'{side}TB2')
        includedMarkers.append(f'{side}TB3')
        includedMarkers.append(f'{side}LFC')
        includedMarkers.append(f'{side}MFC')
        includedMarkers.append(f'{side}LMAL')
        includedMarkers.append(f'{side}MMAL')
        includedMarkers.append(f'{side}HJC')
        includedMarkers.append(f'{side}KJC')
        includedMarkers.append(f'{side}EJC')
        includedMarkers.append(f'{side}AJC')
        includedMarkers.append(f'{side}SJC')

    return includedMarkers


def create_markers_table(model, states_trajectory):

    includedMarkers = get_markers_list()
    model.initSystem()
    markersTable = osim.TimeSeriesTableVec3()
    numStates = states_trajectory.getSize()

    markerSet = model.getMarkerSet()
    numMarkers = markerSet.getSize()
    for istate in range(numStates):
        state = states_trajectory.get(istate)
        model.realizePosition(state)
        row = osim.RowVectorVec3(len(includedMarkers))
        for imarker, marker_name in enumerate(includedMarkers):
            marker = markerSet.get(marker_name)
            row[imarker] = marker.getLocationInGround(state)

        markersTable.appendRow(state.getTime(), row)

    # Create table.
    labels = osim.StdVectorString()
    for marker_name in includedMarkers:
        labels.append(marker_name)

    markersTable.setColumnLabels(labels)

    time = np.array(markersTable.getIndependentColumn())
    dt = time[1] - time[0]
    datarate = 1 / dt
    markersTable.addTableMetaDataString('DataRate', str(datarate))
    markersTable.addTableMetaDataString('Units', 'm')

    return markersTable


def create_static_trial_markers(model):

    includedMarkers = get_markers_list()

    state = model.initSystem()
    markersTable = osim.TimeSeriesTableVec3()

    markerSet = model.getMarkerSet()
    numMarkers = markerSet.getSize()

    coordSet = model.updCoordinateSet()
    for icoord in range(coordSet.getSize()):
        coord = coordSet.get(icoord)
        coordName = coord.getName()
        if coordName == 'pelvis_ty':
            coord.setValue(state, 0.93)
        # elif 'arm_add' in coordName:
        #     coord.setValue(state, -90.0 * (3.14159 / 180.0))
        else:
            coord.setValue(state, 0.0)

    model.realizePosition(state)
    row = osim.RowVectorVec3(len(includedMarkers))
    for imarker, marker_name in enumerate(includedMarkers):
        marker = markerSet.get(marker_name)
        row[imarker] = marker.getLocationInGround(state)

    markersTable.appendRow(state.getTime(), row)

    # Create table.
    labels = osim.StdVectorString()
    for marker_name in includedMarkers:
        labels.append(marker_name)

    markersTable.setColumnLabels(labels)

    time = np.array(markersTable.getIndependentColumn())
    markersTable.addTableMetaDataString('DataRate', '100.0')
    markersTable.addTableMetaDataString('Units', 'm')

    return markersTable


def create_coordinates_from_solution(solution_fpath):
    solution = osim.TimeSeriesTable(solution_fpath)
    coordinates = osim.TimeSeriesTable(solution.getIndependentColumn())
    for label in solution.getColumnLabels():
        if 'beta' in label: continue
        if '/value' in label:
            newLabel = copy.deepcopy(label)
            newLabel = newLabel.replace('/value', '')
            newLabel = os.path.basename(newLabel)
            coordinates.appendColumn(newLabel, solution.getDependentColumn(label))

    return coordinates


def fill_analysis_template(template, setup, subject, results,
                           startTime, endTime, extLoads, coordinates):
    ft = open(template)
    content = ft.read()
    content = content.replace('@TRIAL@', f'{subject}_walk2')
    content = content.replace('@MODEL@', f'{subject}.osim')
    content = content.replace('@RESULTS_DIR@', results)
    content = content.replace('@START_TIME@', f'{startTime:.2f}')
    content = content.replace('@END_TIME@', f'{endTime:.2f}')
    content = content.replace('@EXT_LOADS@', extLoads)
    content = content.replace('@COORDINATES@', coordinates)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


def fill_extloads_template(template, setup, subject):
    ft = open(template)
    content = ft.read()
    content = content.replace('@SUBJECT@', subject)

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


def fill_id_template(template, setup, subject, start_time, end_time):
    ft = open(template)
    content = ft.read()
    content = content.replace('@MODEL@', f'{subject}.osim')
    content = content.replace('@SUBJECT@', subject)
    content = content.replace('@START_TIME@', f'{start_time:.2f}')
    content = content.replace('@END_TIME@', f'{end_time:.2f}')

    ft.close()
    f = open(setup, 'w')
    f.write(content)
    f.close()


# Create a function to remove columns from two DataFrames that are not in both DataFrames.
def remove_columns_not_in_both(df1, df2):
    """Remove columns from two DataFrames that are not in both DataFrames."""
    df1_cols = set(df1.columns)
    df2_cols = set(df2.columns)
    cols_to_remove = df1_cols - df2_cols
    df1 = df1.drop(columns=cols_to_remove)
    cols_to_remove = df2_cols - df1_cols
    df2 = df2.drop(columns=cols_to_remove)
    return df1, df2




