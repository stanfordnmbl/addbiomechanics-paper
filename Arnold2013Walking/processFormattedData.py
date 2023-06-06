import pandas as pd
import subprocess

def processFormattedData():
    demographics_df = pd.read_csv('demographics.csv')
    subjects = demographics_df['subject']
    for subject in subjects:
        subprocess.call(['./run_engine.sh', subject])

if __name__ == "__main__":
    processFormattedData()