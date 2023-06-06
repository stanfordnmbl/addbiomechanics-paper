#!/bin/bash

python formatAndCopyData.py
python fillAndCopySubjectJSON.py
python processFormattedData.py
python computeResultsAcrossSubjects.py
python createFilesForResiduals.py
python calculateResiduals.py addbio
python processOpenCapResults.py
python calculateResiduals.py opencap
python plotMarkerErrorsAndResiduals.py
python plotJointAnglesAndTorques.py