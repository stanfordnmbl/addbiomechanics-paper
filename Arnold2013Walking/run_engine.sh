#!/bin/bash

# Grab the subject identifier via the passed in argument.
SUBJECT_ID="$1"

# Get path to a local install of AddBiomechanics (needed to run engine.py).
ADDBIO_PATH=/home/nbianco/repos/AddBiomechanics

# Process the data:
#   1. If an existed 'Processed' folder for this subject exists, remove it.
#   2. Copy the subject folder from 'Formatted' to 'Processed', where we can freely modify it.
#   3. Copy over the model Geometry folder to the subject's 'Processed' folder.
#   4. Run engine.py.
CURR_DIR=`pwd`
echo $CURR_DIR
rm -rf $CURR_DIR/Processed/${SUBJECT_ID}
cp -r $CURR_DIR/Formatted/${SUBJECT_ID} $CURR_DIR/Processed/${SUBJECT_ID}
cp -r $CURR_DIR/Raw/Geometry $CURR_DIR/Processed/${SUBJECT_ID}/Geometry
python $ADDBIO_PATH/server/engine/engine.py $CURR_DIR/Processed/${SUBJECT_ID}