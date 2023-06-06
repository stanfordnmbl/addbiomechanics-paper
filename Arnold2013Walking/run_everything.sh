#!/bin/bash

#python runInverseDynamics.py
python reregisterScaledModelMarkers.py
python formatAndCopyData.py
python fillAndCopySubjectJSON.py True
python processFormattedData.py
python computeResultsAcrossSubjects.py
python createFilesForResiduals.py
python calculateResiduals.py addbio
python plotComparisons.py
python plotFigure.py