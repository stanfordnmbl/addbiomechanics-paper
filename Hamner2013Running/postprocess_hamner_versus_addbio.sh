#!/bin/bash

conda activate addbio
python processAddBiomechanicsResults.py
python copyHamnerData.py
python processHamnerResults.py